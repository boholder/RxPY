from rx import Observable, AnonymousObservable
from rx.internal import extends

@extends(Observable)
class TakeLastBuffer(object):


    def take_last_buffer(self, count):
        """Returns an array with the specified number of contiguous elements
        from the end of an observable sequence.

        Example:
        res = source.take_last(5)

        Description:
        This operator accumulates a buffer with a length enough to store
        elements count elements. Upon completion of the source sequence, this
        buffer is drained on the result sequence. This causes the elements to be
        delayed.

        Keyword arguments:
        count -- {Number} Number of elements to take from the end of the source
            sequence.

        Returns an observable {Observable} sequence containing a single array
        with the specified number of elements from the end of the source
        sequence.
        """

        source = self

        def subscribe(observer):
            q = []
            def on_next(x):
                with self.lock:
                    q.append(x)
                    if len(q) > count:
                        q.pop(0)

            def on_completed():
                observer.on_next(q)
                observer.on_completed()

            return source.subscribe(on_next, observer.on_error, on_completed)
        return AnonymousObservable(subscribe)
