# AWS websocket example

During innovation week at work I decided to do some hands on from-the-ground-up work on implementing websockets in aws. This also ended up being an intro-to-building-via-serverless project for me. I've worked in serverless codebases for years now, but I've never set one up from scratch and I didn't know some of the nuances of building with serverless (hard to get those exp points when you work in projects that are already setup :/ ).

So, this codebase for me is:
- Setting up a serverless project from scratch
- Building out the infrastructure needed for a simple websocket setup using api gateway, lambdas, and dynamodb 
- Learning the serverless cli tools, _maybe_ diving into the serverless application model if there's enough time

# Up and running

## Deploying to AWS
The severless deployment depends on what AWS credentials you're using locally. If you've pulled down the dev credentials it will deploy to the dev **account**, if you have the prod credentials it will deploy to the prod **account**. 

Note that while I added a `stage` configuration in the serverless.yml file I haven't piped that in everwhere, so while you'll see the `-dev` suffix pop up on most things it's not on everything yet (and really, this should only live in dev so I'm not in a hurry to pop it in everywhere).

```commandline
# deploy to aws
sls deploy

# destroy aws infrastructure
sls remove
```

# Demo highlights

- Direct serverless deploy
  - Watching cloudformation
  - Addressing cloudformation snags more gracefully
    - E.g. a resource that can't be created b/c it can't be renamed -> sls remove and then deploy (our cicd doesn't do that (double check))
- API Gateway/Websocket nuances
  - The route expression is prefixed with `$request.body.<...>`
    - `request` is the request event, not a property 
    - `body` is the event property body, but it's automatically added
    - `<...>` is whatever json property you actually want to use, so when you see examples like `$request.body.action`, your message payload just needs `{"action":"some-action"}`