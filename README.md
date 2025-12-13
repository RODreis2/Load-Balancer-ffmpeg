--FFmpeg Local Task Load Balancer (Thread-Based)

This project is a local task dispatcher and load balancer for FFmpeg jobs, implemented in Python using threads and a task queue.
Its main goal is to process multiple video encoding tasks concurrently, distributing them across a fixed number of worker threads while maintaining a simple and predictable architecture.



--Project Purpose

- The objective of this project is learning-oriented, focusing on:

- Understanding concurrency and parallel execution

- Applying the Producer–Consumer pattern

- Managing external processes (FFmpeg)

- Designing a simple load balancing mechanism

- Being able to fully explain the system design and execution flow

- This is a local system, not distributed, by design.



--High-Level Architecture

The system is composed of four main components:

[File Producer]
      ↓
[Task Queue]
      ↓
[Worker Threads]
      ↓
[FFmpeg Subprocess]

Component Responsibilities

Producer (Main Thread)
Discovers input video files and pushes them into a shared queue.

Task Queue (queue.Queue)
Acts as a synchronization-safe buffer between the producer and worker threads.

Worker Threads
Consume tasks from the queue and execute FFmpeg commands.

FFmpeg Subprocess
Performs the actual video conversion.
