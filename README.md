# Slang challenge
This challenge consist in 3 steps:

1. Get the data from the slang's API
2. Process the data so that we can generate new data that contains user sessions
3. Post the data to slang's API

## Considerations:
The algorithm it could be better if we consider the data organized, It had to be implemented a previous algorithm (Heap Sort) so that It could be ordered the data received.
Therefor the complexity of the algorithm proposed increase from $ O(n \cdot m) $ to $ O(n \cdot m \cdot \log(m)) $ such that n depends on the number of users and m depends on the number of activities.

Notice that that the number of users and the number of activities were differentiated, in order to deal with the worst cases separately by applying divide and conquer.
