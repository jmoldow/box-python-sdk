# coding: utf-8

from __future__ import unicode_literals

from functools import wraps
from itertools import chain
from operator import itemgetter

from requests.exceptions import Timeout
from six.moves import filter, map

from boxsdk.object.base_endpoint import BaseEndpoint
from boxsdk.util.lru_cache import LRUCache


def _filter_out_already_seen_event_ids_from_yielded_event_lists(func):
    event_ids = LRUCache()

    def is_new_event(event):
        try:
            event_ids.get(event['event_id'])
            return False
        except KeyError:
            return True

    @wraps(func)
    def wrapper(*args, **kwargs):
        for events in func(*args, **kwargs):
            new_events = list(filter(is_new_event, events))
            yield new_events
            for new_event in new_events:
                event_ids.set(new_event['event_id'])

    return wrapper


def _use_latest_stream_position_if_none(func):

    @wraps(func)
    def wrapper(self, stream_position=None, *args, **kwargs):
        stream_position = stream_position if (stream_position is not None) else self.get_latest_stream_position()
        return func(self, stream_position=stream_position, *args, **kwargs)

    return wrapper


class Events(BaseEndpoint):
    """Box API endpoint for subscribing to changes in a Box account."""

    def get_url(self, *args):
        """Base class override."""
        return super(Events, self).get_url('events', *args)

    def get_events(self, limit=100, stream_position=0, stream_type='all'):
        """
        Get Box events from a given stream position for a given stream type.

        :param limit:
            Maximum number of events to return.
        :type limit:
            `int`
        :param stream_position:
            The location in the stream from which to start getting events. 0 is the beginning of time. 'now' will
            return no events and just current stream position.
        :type stream_position:
            `unicode`
        :param stream_type:
            Which type of events to return. Can be 'all', 'tree', or 'sync'.
        :type stream_type:
            `unicode`
        :returns:
            JSON response from the Box /events endpoint. Contains the next stream position to use for the next call,
            along with some number of events.
        :rtype:
            `dict`
        """
        url = self.get_url()
        params = {
            'limit': limit,
            'stream_position': stream_position,
            'stream_type': stream_type,
        }
        box_response = self._session.get(url, params=params)
        return box_response.json()

    def get_latest_stream_position(self):
        """
        Get the latest stream position. The return value can be used with :meth:`get_events` or
        :meth:`generate_events_with_long_polling`.

        :returns:
            The latest stream position.
        :rtype:
            `unicode`
        """
        url = self.get_url()
        params = {
            'stream_position': 'now',
        }
        return self._session.get(url, params=params).json()['next_stream_position']

    def _get_all_events_since(self, stream_position):
        next_stream_position = stream_position
        events = []
        get_event_id = itemgetter('event_id')

        def is_new_event(event):
            return get_event_id(event) not in map(get_event_id, events)

        while True:
            response = self.get_events(stream_position=next_stream_position, limit=100)
            next_stream_position = response['next_stream_position']
            new_events = response['entries']
            events.extend(filter(is_new_event, new_events))
            if not new_events:
                return events, next_stream_position

    def long_poll(self, options, stream_position):
        """
        Set up a long poll connection at the specified url.

        :param options:
            The long poll options which include a long pull url, retry timeout, etc.
        :type options:
            `dict`
        :param stream_position:
            The location in the stream from which to start getting events. 0 is the beginning of time.
            'now' will return no events and just current stream position.
        :type stream_position:
            `unicode`
        :returns:
            {"message": "new_change"}, which means there're new changes on Box or {"version": 1, "message": "reconnect"}
            if nothing happens on Box during the long poll.
        :rtype:
            `dict`
        """
        url = options['url']
        long_poll_response = self._session.get(
            url,
            timeout=options['retry_timeout'],
            params={'stream_position': stream_position}
        )
        return long_poll_response

    def generate_events_with_long_polling(self, stream_position=None):
        """
        Subscribe to events from the given stream position.

        :param stream_position:
            The location in the stream from which to start getting events. 0 is the beginning of time. 'now' will
            return no events and just current stream position.
        :type stream_position:
            `unicode`
        :returns:
            Events corresponding to changes on Box in realtime, as they come in.
        :rtype:
            `generator` of :class:`Event`
        """
        return chain.from_iterable(self.generate_event_lists_with_long_polling(stream_position=stream_position))

    @_filter_out_already_seen_event_ids_from_yielded_event_lists
    @_use_latest_stream_position_if_none
    def generate_event_lists_with_long_polling(self, stream_position):
        while True:
            options = self.get_long_poll_options()
            while True:
                try:
                    long_poll_response = self.long_poll(options, stream_position)
                except Timeout:
                    break
                else:
                    message = long_poll_response.json()['message']
                    if message == 'new_change':
                        events, stream_position = self._get_all_events_since(stream_position)
                        yield events
                        break
                    elif message == 'reconnect':
                        continue
                    else:
                        break

    @_filter_out_already_seen_event_ids_from_yielded_event_lists
    @_use_latest_stream_position_if_none
    def generate_event_lists_with_manual_polling(self, stream_position):
        while True:
            events, stream_position = self._get_all_events_since(stream_position)
            yield events

    def get_long_poll_options(self):
        """
        Get the url and retry timeout for setting up a long polling connection.

        :returns:
            A `dict` including a long poll url, retry timeout, etc.
            E.g.
                {
                    "type": "realtime_server",
                    "url": "http://2.realtime.services.box.net/subscribe?channel=cc807c9c4869ffb1c81a&stream_type=all",
                    "ttl": "10",
                    "max_retries": "10",
                    "retry_timeout": 610,
                }
        :rtype:
            `dict`
        """
        url = self.get_url()
        box_response = self._session.options(url)
        return box_response.json()['entries'][0]
