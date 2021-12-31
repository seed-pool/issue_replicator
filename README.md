# Issue Replicator

This is a GitHub Actions that replicate issues to other repositories by simply labeling them.

## Usage

Set up the GitHub Actions configuration file as follows.

```yaml
name: Issue Replicator

on:
  issues:
    types:
      - labeled

jobs:
  IssueReplicator:
    if: github.event.label.name == 'issue_replicator'
    runs-on: ubuntu-latest
    steps:
      - name: IssueReplicator
        uses: shimewtr/issue_replicator@main
        env:
          GITHUB_ACCESS_TOKEN: ${{secrets.ISSUE_REPLICATOR_TOKEN}}
          GITHUB_ISSUE_NUMBER: ${{ github.event.issue.number }}
          GITHUB_REPOSITORY: ${{ github.repository }}
          ISSUE_REPLICATOR_LABEL: issue_replicator
          REPOSITORY_BY_LABEL: '{"replicate_A": "owner/repoA","replicate_B": "owner/repoB"}'
```

Give a label to fire the workflow and a label to determine the repository to be replicated to.
In the above configuration, the issue will be replicated in the `owner/repoA` repository when the `issue_replicator` and `replicate_A` labels are given.

## Inputs

| Name | Description | Example |
| ---- | ---- | ----- |
| GITHUB_ACCESS_TOKEN | Set up a token with permissions to create issues to the repository you want to replicate. | `${{secrets.ISSUE_REPLICATOR_TOKEN}}` |
| GITHUB_ISSUE_NUMBER | You need to specify the id of the issue. | `${{ github.event.issue.number }}` |
| GITHUB_REPOSITORY | Specify the repository from which you want to replicate. | `${{ github.repository }}` |
| ISSUE_REPLICATOR_LABEL | Specify the label name to fire the workflow. | `issue_replicator` |
| REPOSITORY_BY_LABEL | Specify the label and the repository to be replicated in json format. | `'{"replicate_A": "owner/repoA","replicate_B": "owner/repoB"}'` |
