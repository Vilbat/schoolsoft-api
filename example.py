from schoolsoft import Schoolsoft


schoolsoft = Schoolsoft('username', 'password')


assignments = schoolsoft.get_sorted_assignments()
newest_assignment = schoolsoft.get_newest_assignment()

for i in assignments:
    print(i.name)
    print(i.description)
    print(i.end_date)
    print(i.assignment_type)
    print('\n')