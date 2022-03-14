Project to build docker base images and push to the internal docker registry.

**Note:** Use the `master` branch for latest images and the `node-migration` branch for migration images.

### main NodeJS base images:
change the Docker files under the node directory to update base images. After you push your changes the gitlab CI will create the new image and push it into the docker registry.
the images will be:  
`node:latest`  
`fronend:latest`

### migration NodeJS images:
checkout to the node-migration branch.
change the Docker files under the node directory:
`frontend.migration.Dockerfile`  
`node.migration.Dockerfile`  
* **Note**: these files only exist in the migration branch NOT in Master.  

make you changes and push the branch will create 2 new migration images into the registry:
`frontend:migration`  
`node:migration`
