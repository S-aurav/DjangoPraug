import asyncio

async def fetch_data(delay):
    print("Fetching data...")
    await asyncio.sleep(delay)
    print("Data fetched")
    return {"data": "Some data"}

async def main():
    print("Start of main coroutines")
    task = fetch_data(2)
    # Await the fetch_data coroutine, pausing execution of main until fetach_data completes
    result = await task
    print(f"Received result: {result}")
    print("End of main coroutine")


async def fetch_data(delay, id):
    print("Fetching data... id: ", id)
    await asyncio.sleep(delay)
    print("Data fetched, id:", id)
    return {"data": "Some data", "id": id}

async def main():
    task1 = fetch_data(2, 1)
    task2 = fetch_data(2, 2)

    result1 = await task1
    print(f"Received result: {result1}")

    result2 = await task2
    print(f"Received result: {result2}")


async def fetch_data(id, sleep_time):
    print(f"Coroutine {id} starting to fetch data.")
    await asyncio.sleep(sleep_time)
    return {"id": id, "data": f"Sample data from coroutine {id}"}

async def main():
    # Create tasks for running coroutines concurrently
    task1 = asyncio.create_task(fetch_data(1, 2))
    task2 = asyncio.create_task(fetch_data(2, 3))
    task3 = asyncio.create_task(fetch_data(3, 1))

    result1 = await task1
    result2 = await task2
    result3 = await task3

    print(result1, result2, result3)


async def main():
    # Run coroutines concurrently and gather their return values
    results = await asyncio.gather(fetch_data(1, 2), fetch_data(2, 1), fetch_data(3, 3))

    #Process the results
    for result in results:
        print(f"Received resuilt: {result}")

# TaskGroup provides built-in error handling and cancellation
async def main():
    tasks = []
    async with asyncio.TaskGroup() as tg:
        for i, sleep_time in enumerate([2,1,3], start=1):
            task = tg.create_task(fetch_data(i, sleep_time))
            tasks.append(task)

    # After the Task Group block, all tasks are completed
    results = [task.result() for task in tasks]

    for result in results:
        print(f"Received result: {result}")


#Future
async def set_future_result(future, value):
    await asyncio.sleep(2)
    #Set the result of the future
    future.set_result(value)
    print(f"Set the future's result to: {value}")

async def main():
    #Create a future object
    loop = asyncio.get_running_loop()
    future = loop.create_future()

    # Schedule setting the future's result
    asyncio.create_task(set_future_result(future, "Future result is ready"))

    # Wait for the future to be set
    result = await future
    print(f"Received future's result: {result}")


# Synchronization

# A shared variable
shared_resource = 0

# An asyncio Lock
lock = asyncio.Lock()

async def modify_shared_resources():
    global shared_resource
    async with lock:
        #Critical section starts
        print(f"Resource before modification: {shared_resource}")
        shared_resource += 1
        await asyncio.sleep(1)
        print(f"Resource after modification: {shared_resource}")
        #Critical section ends

async def main():
    await asyncio.gather(*(modify_shared_resources() for _ in range(5)))


# Semaphore

async def access_resource(semaphore, resource_id):
    async with semaphore:
        # Simulate accessing a limited resource
        print(f"Accessing resource {resource_id}")
        await asyncio.sleep(3)
        print(f"Releasing resource {resource_id}")

async def main():
    semaphore = asyncio.Semaphore(3) # Allow only 2 coroutines to access the resource at a time
    await asyncio.gather(*(access_resource(semaphore, i) for i in range(5)))


# Event

async def waiter(event):
    print("waiting for the event to be set")
    await event.wait()
    print("event has been set, counting execution")

async def setter(event):
    await asyncio.sleep(2)
    event.set()
    print("event has been set!")

async def main():
    event = asyncio.Event()
    await asyncio.gather(waiter(event), setter(event))

asyncio.run(main())