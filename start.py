import docker
client = docker.DockerClient(base_url='tcp://192.168.2.138:2375')
for image in client.images.list():
	print image.id
