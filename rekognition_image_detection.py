# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

"""
Purpose

Shows how to use the AWS SDK for Python (Boto3) with Amazon Rekognition to
recognize people, objects, and text in images.

The usage demo in this file uses images in the .media folder. If you run this code
without cloning the GitHub repository, you must first download the image files from
    https://github.com/awsdocs/aws-doc-sdk-examples/tree/master/python/example_code/rekognition/.media
"""

import logging
from pprint import pprint
import boto3
from botocore.exceptions import ClientError
import requests


class RekognitionImage:
    """
    Encapsulates an Amazon Rekognition image. This class is a thin wrapper
    around parts of the Boto3 Amazon Rekognition API.
    """
    def __init__(self, image, image_name, rekognition_client):
        """
        Initializes the image object.

        :param image: Data that defines the image, either the image bytes or
                      an Amazon S3 bucket and object key.
        :param image_name: The name of the image.
        :param rekognition_client: A Boto3 Rekognition client.
        """
        self.image = image
        self.image_name = image_name
        self.rekognition_client = rekognition_client

    @classmethod
    def from_bucket(cls, s3_object, rekognition_client):
        """
        Creates a RekognitionImage object from an Amazon S3 object.

        :param s3_object: An Amazon S3 object that identifies the image. The image
                          is not retrieved until needed for a later call.
        :param rekognition_client: A Boto3 Rekognition client.
        :return: The RekognitionImage object, initialized with Amazon S3 object data.
        """
        image = {'S3Object': {'Bucket': s3_object.bucket_name, 'Name': s3_object.key}}
        return cls(image, s3_object.key, rekognition_client)



    def detect_labels(self, max_labels):
        """
        Detects labels in the image. Labels are objects and people.

        :param max_labels: The maximum number of labels to return.
        :return: The list of labels detected in the image.
        """
        try:
            response = self.rekognition_client.detect_labels(
                Image=self.image, MaxLabels=max_labels)
            labels = []
            for label in response['Labels']:
                print(label.get('Name'), label.get('Confidence'))
                labels.append(label.get('Name'))
        except ClientError:
            raise
        else:
            return labels




def usage_demo():
    print('-'*88)
    print("Welcome to the Amazon Rekognition image detection demo!")
    print('-'*88)

    bucket_name = "unr-cs442"

    rekognition_client = boto3.client('rekognition')
    s3 = boto3.resource('s3')
    my_bucket = s3.Bucket(bucket_name)
    for my_bucket_object in my_bucket.objects.all():
        street_object = boto3.resource('s3').Object(bucket_name, my_bucket_object.key)
        street_scene_image = RekognitionImage.from_bucket(street_object, rekognition_client)
        print(f"Detecting labels in {street_scene_image.image_name}...")
        labels = street_scene_image.detect_labels(100)
        print(f"Found {len(labels)} labels.")
        #print(my_bucket_object)

    print("Thanks for watching!")
    print('-'*88)


if __name__ == '__main__':
    usage_demo()
