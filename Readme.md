# Remove unmapped reads document

## Quick start

1. Copy the directory `/kcproject/zhangxinyue/test` to your project folder, 

2. Edit the file `Master.Remove_unmapped.py` and fill the sample name which you want to remove reads, 

3. Edit the file `Master.Remove_unmapped.py` and choose the right project type such as `UID` or `Non-UID`,

4. Execute the following command to remove unmapped reads.

```
    /nas/software/anaconda3/bin/snakemake \ 
    -ps /ur_dir/test/master/Master.Remove_unmapped.py  \ 
    --configfile /ur_dir/project.yaml \
    -j 3 --directory /ur_dir \
    --cluster 'sbatch -c {cluster.threads} -o {cluster.stdout} -e {cluster.stderr} --parsable' \
    --cluster-config /ur_dir/test/pipeline.yaml
```

