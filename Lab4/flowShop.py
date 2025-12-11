class FlowShop():
    def __init__(self, jobs: int, machines: int):
        self.jobs = jobs
        self.machines = machines
        self.processing_times = [[0 for _ in range(self.jobs)] for _ in range(self.machines)]
        self.completion_times = [[0 for _ in range(self.jobs)] for _ in range(self.machines)]
        self.upper_bound = 0
        self.lower_bound = 0
        self.c_max = 0

    def instance_from_file(self, path: str) -> None:
        """
            Load flow shop problem instance from text file.

            Args:
                path (str): path to file with instance
            Returns:
                list[int][int]: processing times for n jobs on m machines
        """

        # Initialize empty 2d array of size jobs x machines
        processing_times = [[0 for _ in range(self.jobs)] for _ in range(self.machines)]

        with open(path, 'r') as file:
            lines = file.readlines()

            for i, line in enumerate(lines):
                processing_times[i] = [int(x) for x in line.strip().split()]

        self.processing_times = processing_times

    def target_function(self, permutation: list[int]) -> int:
        # Initialize empty 2d array of size jobs x machines
        completion_times = [[0 for _ in range(self.jobs)] for _ in range(self.machines)]

        # Calculate completions times for first job only:
        first_job = permutation[0]
        completion_times[0][0] = self.processing_times[0][first_job]

        for m in range(1, self.machines):
            # completion time for 1st job on m machine is equal to 
            # sum of previous completion time and current processing time
            completion_times[m][0] = completion_times[m-1][0] + self.processing_times[m][first_job]

        # Calculate completion times for the rest of jobs
        for j in range(1, self.jobs):
            
            for m in range(1, self.machines):
                # Fisrt machine: just add previous processing time
                completion_times[0][j] = completion_times[0][j-1] + self.processing_times[0][permutation[j]]

                # Any other machine: max of previous job completion time and 
                # current job completion time on previous machine + current processing time
                completion_times[m][j] = max(
                    completion_times[m][j-1],
                    completion_times[m-1][j]
                ) + self.processing_times[m][permutation[j]]

        self.c_max = completion_times[-1][-1]
        self.completion_times = completion_times

        return self.c_max
    
if __name__ == '__main__':
    instance = FlowShop(20, 5)
    instance.instance_from_file("instances.txt")
    c_max = instance.target_function(permutation=[x for x in range(20)])