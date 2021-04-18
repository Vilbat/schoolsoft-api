import requests, datetime, json

from assignment_type import Assignment
import traceback
import threading


class Schoolsoft:
    def __init__(self, username, password, multithreading=False):
        print("Class initialized")
        self.username = username
        self.password = password
        self.multithreading = multithreading

        self.subjects = 19

        self.session = requests.Session()
        self.login_url = 'https://sms14.schoolsoft.se/engelska/jsp/Login.jsp'
        self.subject_url = 'https://sms14.schoolsoft.se/engelska/rest/planning/student/container/{0}/0/0'

        data = {
            'action': 'login',
            'usertype': '1',
            'ssusername': username,
            'sspassword': password,
            'button': 'Login'
        }
        self.session.post(self.login_url, data=data)
        self.results = []

    def parse_assignments(self, unparsed_json):
        results = []

        assignments = unparsed_json['planningDetails']
        for assignment in assignments:
            name = assignment['name']
            description = assignment['description']
            echo = assignment['periods'][0]['endDate']
            end_date = datetime.datetime.fromtimestamp(echo / 1000)
            assignment_type = assignment['tests'][0]['typeName']

            datetime_now = datetime.datetime.now()

            if (end_date - datetime_now).days > 0:
                assignment_object = Assignment(name, description, end_date, assignment_type, echo)
                results.append(assignment_object)
            else:
                return results

        return results

    def get_assignments_from_class(self, i):
            try:
                response = self.session.get(self.subject_url.format(i))
                response_json = response.json()

                parsed_subjects = self.parse_assignments(response_json)
                #return parsed_subjects
                self.results.append(parsed_subjects)
            except Exception as e:
                print(traceback.format_exc())

    def get_assignments(self):
        self.results = []

        threads = []

        for i in range(self.subjects):
            if self.multithreading:
                t = threading.Thread(target=lambda : self.get_assignments_from_class(i))
                t.daemon = True
                threads.append(t)
            else:
                self.get_assignments_from_class(i)
        if self.multithreading:
            for i in range(self.subjects):
                threads[i].start()

            for i in range(self.subjects):
                threads[i].join()
        return [i for sublist in self.results for i in sublist]


    def get_sorted_assignments(self):
        assignments = self.get_assignments()

        assignments.sort(key = lambda x : x.echo)
        return assignments

    def get_newest_assignment(self):
        return self.get_sorted_assignments()[0]

    def get_assignment_type(self, requested_type):
        return list(filter(lambda i : i.assignment_type == requested_type, self.get_sorted_assignments()))