import logging
from collections.abc import Callable
from functools import lru_cache, partial

logger = logging.getLogger("di")


class FutureService:
    """
    A service class that represents a future service with a given signature.

    Attributes:
        _signature (str): The signature of the future service.

    Methods:
        __repr__(): Returns a string representation of the FutureService instance.
    """

    def __init__(self, signature) -> None:
        """
        Initializes the FutureService with a given signature.

        Args:
            signature (str): The signature of the future service.
        """
        self._signature = signature

    def __repr__(self) -> str:
        return f"FutureService({self._signature})"


class Container:
    """
    A service container class that manages the lifecycle and dependencies of services.

    The `Container` class allows you to register service instances, retrieve cached instances,
    and initialize dependencies for services. It provides methods to add services, get cached
    instances, and spin up the services by injecting their dependencies.

    Attributes:
        _services (list): A list to store the registered services and their instances.

    Methods:
        add(signature: str, instance: object) -> None:
        get_cached_instance(instance: object) -> Type[object]:
        get(required_signature: object) -> Callable:
        spinup() -> None:
    Examples:
        >>> container = Container()
        >>> container.add('database', DatabaseService())
        >>> container.add('cache', CacheService())
        >>> db_service = container.get('database')()
        >>> cache_service = container.get('cache')()
        >>> container.spinup()
    """

    def __init__(self) -> None:
        self._services: list = []

    def add(self, signature, instance):
        """
        Adds a service instance to the service container.

        Args:
            signature (str): The unique identifier for the service.
            instance (object): The instance of the service to be added.

        Returns:
            None
        """
        logger.debug(f"Instance for {signature} added as {instance}")
        self._services.append((signature, instance))

    @staticmethod
    @lru_cache(typed=True)
    def get_cached_instance(instance) -> type[object]:
        """
        Retrieve and return a cached instance.

        Args:
            instance: The instance to be retrieved from the cache.

        Returns:
            Type[object]: The cached instance.
        """
        logger.debug(f"Returning instance {instance}")
        return instance

    def get(self, required_signature: object) -> Callable:
        """
        Retrieve a cached instance of a service based on the required signature.

        Args:
            required_signature (object): The signature of the required service.

        Returns:
            Callable: A partial function that returns the cached instance of the service.

        Raises:
            ValueError: If no service with the required signature is found.
        """
        for signature, instance in self._services:
            if signature is required_signature:
                return partial(self.get_cached_instance, instance)
        raise ValueError("No service %s found" % required_signature)

    def spinup(self):
        """
        Initializes and injects dependencies for services.

        This method iterates over the registered services and their properties.
        If a property is an instance of FutureService, it replaces it with an
        initialized service instance based on the signature.
        You are required to call this method before using the services.

        Raises:
            AttributeError: If a property does not exist on the instance.
            TypeError: If the property is not an instance of FutureService.
        """
        for signature, instance in self._services:
            for property in dir(instance):
                try:
                    if isinstance(getattr(instance, property), FutureService):
                        setattr(
                            instance,
                            property,
                            self.get(getattr(instance, property)._signature)(),
                        )
                except AttributeError:
                    continue
            logger.debug(f"Service {signature} is {instance}")


    async def run_postspinup(self):
        """
        Runs the post-spinup method for services.

        This method iterates over the registered services and checks if they have a post-spinup method.
        If a service has a post-spinup method, it is called asynchronously.
        """
        for signature, instance in self._services:
            if hasattr(instance, "post_spinup"):
                logger.debug(f"Running post-spinup for {signature}")
                await instance.post_spinup()
