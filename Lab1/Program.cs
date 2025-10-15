using System;
using System.Threading;
using System.Threading.Tasks;

namespace Semaphore
{
    class Program
    {
        static int cole = 2000;
        static int warehouse = 0;
        static int numberOfMiners = 5;
        static int vechicleCapacity = 200;

        static SemaphoreSlim semaphoreMine = new SemaphoreSlim(2, 2);
        static SemaphoreSlim semaphoreWarehouse = new SemaphoreSlim(1, 1);
        static object lockObject = new object();

        static void Main (string [] args)
        {
            Task[] tasks = new Task[numberOfMiners];

            for (int i = 0; i < tasks.Length; i++)
            {
                tasks[i] = Task.Run(() => minerWork());
            }
            
            Task.WaitAll(tasks);
            Console.WriteLine("Zloze wegla na koncu: " + cole);
            Console.WriteLine("Magazyn na koncu: " + warehouse);
        }
        static void minerWork()
        {
            for (int i = 0; i < numberOfMiners; i++)
            {
                int transportedCoal = 0;

                // Pick up coal.
                semaphoreMine.Wait();
                Thread.Sleep(10);

                lock (lockObject)
                {
                    if (cole > 0)
                    {
                        cole -= vechicleCapacity;
                        transportedCoal = vechicleCapacity;
                        Console.WriteLine($"Gornik {Task.CurrentId} wydobyl {vechicleCapacity} jednostek wegla. Pozostalo: {cole}");
                    }
                }

                semaphoreMine.Release();

                // Transport coal.
                Console.WriteLine($"Gornik {Task.CurrentId} transportuje wegiel do magazynu...");
                Thread.Sleep(10000);

                // Unload coal.
                semaphoreWarehouse.Wait();
                Thread.Sleep(10);

                lock (lockObject)
                {
                    warehouse += transportedCoal;
                    transportedCoal = 0;
                    Console.WriteLine($"Gornik {Task.CurrentId} rozladowuje wegiel. Stan magazynu: {warehouse}");
                }

                semaphoreWarehouse.Release();
            }
        }
    }
}