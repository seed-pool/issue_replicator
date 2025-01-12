import json
import os
from github import Github

GITHUB_ACCESS_TOKEN = os.environ['GITHUB_ACCESS_TOKEN']
GITHUB_REPOSITORY = os.environ['GITHUB_REPOSITORY']
GITHUB_ISSUE_NUMBER = os.environ['GITHUB_ISSUE_NUMBER']
ISSUE_REPLICATOR_LABEL = os.environ['ISSUE_REPLICATOR_LABEL']
REPOSITORY_BY_LABEL = os.environ['REPOSITORY_BY_LABEL']


class IssueReplicator():
    def __init__(self):
        origin = Replicator(GITHUB_REPOSITORY)
        origin.get_issue(int(GITHUB_ISSUE_NUMBER))
        origin_labels = list(map(lambda label: label.name, origin.issue.labels))
        target_repository_by_label = {k: v for k, v in self.parse_repository_by_label().items() if k in origin_labels}
        replicators = [Replicator(repository_name) for repository_name in target_repository_by_label.values() if repository_name]
        list((replicator.replicate_issue(origin.issue) for replicator in replicators))
        list((replicator.add_reference_messages([origin] + replicators) for replicator in [origin] + replicators))
        origin.unlabel(list(target_repository_by_label.keys()) + [ISSUE_REPLICATOR_LABEL])

    def parse_repository_by_label(self):
        try:
            repository_by_label = json.loads(REPOSITORY_BY_LABEL)
        except:
            self.error_handler("REPOSITORY_BY_LABEL is incorrect")
        return repository_by_label


class Replicator():
    def __init__(self, repository_name):
        self.repo = self.get_repo(repository_name)

    def get_issue(self, id):
        self.issue = self.repo.get_issue(id)

    def get_repo(self, repository_name):
        try:
            repo = Github(GITHUB_ACCESS_TOKEN).get_repo(repository_name)
        except:
            self.error_handler("ACCESS_TOKEN does not have permissions to {} repository.".format(repository_name))
        return repo

    def unlabel(self, labels):
        list((self.issue.remove_from_labels(label) for label in labels))

    def error_handler(self, message):
        print('\033[31m' + message + '\033[0m')
        raise Exception

    def reference_message(self):
        return "{} {}\n".format("depends on * ", self.issue.html_url)

    def add_reference_messages(self, replicators):
        body = self.issue.body + "\n" if self.issue.body else ""
        for replicator in replicators:
            if replicator.repo.full_name != self.repo.full_name:
                body += replicator.reference_message()
        self.issue.edit(body=body)

    def replicate_issue(self, origin_issue):
        try:
            self.issue = self.repo.create_issue(origin_issue.title, body=origin_issue.body or "")
        except:
            self.error_handler("Could not create an issue in the {} repository.".format(self.repo.name))


if __name__ == '__main__':
    IssueReplicator()
