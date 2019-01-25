import yaml
import traceback


class Worker(object):
    """ Basic implementation of a generic worker which is intended to be used with the lib_learning.collection
        work scheduler paradigm. The worker recieves work parameters in the form of a dictionary from an interface,
        attempts to do perform the paramterized work, and then reports the result of the work back to the interface.

        Details on the paradigm can be found in the documentation at ib_learning/collections/README.md.

    Inputs:
        interface <lib_learning.collection.interfaces.base_interface.Interface>: A lib_learning.collection Interface
            object from which the worker will recieve
        do_fn <function>: A function mapping a work block in the form of a python dictionary to some work done.
            Thread safety of the do_fn must be managed by the implementor according to their own needs.
        logger <logging.Logger>: A standard python logging object to which worker logs will be written.
    """
    def __init__(self, interface, do_fn, logger):
        self.interface = interface
        self.do_fn = do_fn
        self.logger = logger

        self.main_loop()


    def main_loop(self):
        while True:
            work_block = self.interface.get_work()
            self.logger.info('got new work block\n{}'.format(yaml.dump(kwargs, default_flow_style=False)))

            try:
                self.logger.exception('processing work block {} succeeded'.format(work_block['_retrieval_datetime']))
                self.do_fn(work_block)
                work_block['_status'] = 'SUCCESS'

            except:
                self.logger.exception('processing work block {} failed with exception\n{}'.format(
                    work_block['_retrieval_datetime'],
                    traceback.format_exc()
                ))
                work_block['_status'] = traceback.format_exc()

            self.interface.push_confirmation(work_block)