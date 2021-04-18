from schoolsoft import Schoolsoft
import timeit


schoolsoft = Schoolsoft('username', 'password', multithreading=True)


#print(timeit.timeit(schoolsoft.get_sorted_assignments, number=1))

assignments = schoolsoft.get_sorted_assignments()
newest_assignment = schoolsoft.get_newest_assignment()

for j in assignments:
    print(j.name)
    print(j.description)
    print(j.end_date)
    print(j.assignment_type)
    print('\n')