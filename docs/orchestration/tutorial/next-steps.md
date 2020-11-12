<<<<<<< HEAD
# Conclusion and Next Steps

In this tutorial we covered:

- Creating a project
- Registering and running flows
- Providing flow parameters at runtime
- Altering a flow's execution environment through it's
  [run-config](/orchestration/flow_config/run_configs.md)
- Enabling parallelism by swapping out a flow's
  [executor](/orchestration/flow_config/executors.md).

This is just the beginning; the Prefect API has many more features to explore!

## Concepts

Visit the [Concept](/orchestration/concepts/api.html) docs for actions such as
working directly with Prefect's [GraphQL
API](/orchestration/concepts/graphql.html), diving into the
[CLI](/orchestration/concepts/cli.html), setting [concurrency
limits](/orchestration/concepts/task-concurrency-limiting.html) on your Cloud runs,
and more.

## Agents

To learn more about Prefect agents, [flow
affinity](/orchestration/agents/overview.html#labels) via labels, or find
information on platform specific agents visit the
[agent](/orchestration/agents/overview.html) documentation.

## Flow Configuration

For information on all the options for configuring a flow for deployment, see
the [Flow Configuration](/orchestration/flow_config/overview.html) documentation.

## Deployment Recipes

Check out some of the [deployment
recipes](/orchestration/recipes/configuring_storage.html) that are written
for some example flow deployment patterns.
=======
# Next Steps

So far we've run a flow locally a variety of ways and moved up to distributing the flow execution with Kubernetes and the Prefect API. This is just the beginning because the Prefect API has many more features to explore!

## Concepts

Visit the [Concept](/orchestration/concepts/api.html) docs for actions such as working directly with Prefect's [GraphQL API](/orchestration/concepts/graphql.html), diving into the [CLI](/orchestration/concepts/cli.html), setting [concurrency limits](/orchestration/concepts/concurrency-limiting.html) on your Cloud runs, and more.

## Agents

To learn more about Prefect agents, [flow affinity](/orchestration/agents/overview.html#flow-affinity-labels) via labels, or find information on platform specific agents visit the [agent](/orchestration/agents/overview.html) documentation.

## Storage Options

Store your flows in the cloud using Azure, GCS, or S3! For more information visit the [Storage Options](/orchestration/execution/storage_options.html) documentation.

## Execution Environments

For information related to execution environments take a look at the [execution](/orchestration/execution/overview.html) documentation.

## Deployment Recipes

Check out some of the [deployment recipes](/orchestration/recipes/configuring_storage.html) that are written below for some helpful flow deployment patterns.
>>>>>>> prefect clone
