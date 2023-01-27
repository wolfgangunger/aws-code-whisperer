from constructs import Construct

from aws_cdk import (
    Duration,
    Stack,
    aws_iam as iam,
    aws_sqs as sqs,
    aws_sns as sns,
    aws_sns_subscriptions as subs,
)


class MyStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:

        # create a sqs  queue
        queue = sqs.Queue(
            self, "MyFirstQueue",
            visibility_timeout=Duration.seconds(300),
        )
        # create a sns topic

        # create a topic
        topic = sns.Topic(self, "MyFirstTopic")
        # create a ec2
        ec2 = ec2.Instance(self, "MyFirstEC2")
        # create a rds
        rds = rds.Instance(self, "MyFirstRDS")
        # create a role
        role = iam.Role(self, "MyFirstRole",
                        assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"))
        # create a policy
        policy = iam.Policy(self, "MyFirstPolicy",
                            statements=[
                                iam.PolicyStatement(

                                    effect=iam.Effect.ALLOW,
                                    actions=["ec2:*"],

                                    resources=["*"],
                                    conditions={

                                        "StringEquals": {
                                            "ec2:Region": "us-east-1"
                                        }
                                    }
                                )
                            ])

        # attach policy to role
        role.attach_inline_policy(policy)
        # add policy to role
        role.add_to_policy(policy)
        # add role to instance
        ec2.role = role
        # add topic to queue
        queue.add_event_notification_attributes(

            sqs.QueueEventNotificationAttribute(
                "All",

                "true",
            )
        )
        
