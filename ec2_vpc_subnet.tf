provider "aws" {
    # change region as per your configuration
	region = "us-west-2"
}


resource "aws_vpc" "public-vpc" {
  cidr_block = "10.0.0.0/16"
  enable_dns_hostnames = false
  tags = {
        "name" = "mypublic-vpc"
    }
}

resource "aws_subnet" "public-subnet" {
  vpc_id = "${aws_vpc.public-vpc.id}"
  cidr_block = "10.0.1.0/24"
  availability_zone = "us-west-2a"
  map_public_ip_on_launch = false
  tags = {
        "name" = "mypublic-subnet"
  }

}

resource "aws_security_group" "sgweb" {
  name = "vpc_test_web"
  description = "Allow incoming HTTP connections & SSH access"

  ingress {
    from_port = 80
    to_port = 80
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port = 443
    to_port = 443
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port = -1
    to_port = -1
    protocol = "icmp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port = 22
    to_port = 22
    protocol = "tcp"
    cidr_blocks =  ["0.0.0.0/0"]
  }

  egress {
    from_port       = 0
    to_port         = 0
    # -1 is default and used for ICMP
    protocol        = "-1"
    cidr_blocks     = ["0.0.0.0/0"]
  }

  vpc_id="${aws_vpc.public-vpc.id}"

}

resource "aws_instance" "web" {
	ami = "ami-0c2ab3b8efb09f272"
	instance_type = "t2.micro"
	subnet_id = "${aws_subnet.public-subnet.id}"
	vpc_security_group_ids = ["${aws_security_group.sgweb.id}"]
    tags = {
        "name" = "myEC2-Web"
    }
}
