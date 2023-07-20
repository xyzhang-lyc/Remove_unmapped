#!/usr/bin/env python
# coding: utf-8

if(project_type == "UID"):

	if(ALIGN == "STAR"):

		rule Unmapped_id:
			input:
				reads_id = PROJECT_DIR + "/UID/{samplename}.reads_ids.txt",
				unmapped_mate1 = PROJECT_DIR + "/mapping/{samplename}/Unmapped.out.mate1",
				bam_stat = PROJECT_DIR + "/supp/mapping/bam_stat.xls",
			output:
				unmapped_id = PROJECT_DIR + "/mapping/{samplename}/Unmapped.id.xls",
			threads:
				softconfig["rule_Unmapped_id"]["threads"]
			params:
				select_unmapped = softconfig["rule_Unmapped_id"]["soft"]["select_unmapped"]["path"],
				container = softconfig["rule_Unmapped_id"]["singularity"]["py3"]["path"],
				conargs = softconfig["rule_Unmapped_id"]["singularity"]["py3"]["conargs"],
				python3 = softconfig["rule_Unmapped_id"]["singularity"]["py3"]["soft"]["python3"]["cmd"],
				singularity = softconfig["envs"]["singularity"],
			run:
				shell(
					"{params.singularity} {params.conargs} {BIND_DIRS} {params.container} \
					{params.python3} {params.select_unmapped} -N {input.unmapped_mate1} \
					-B {input.bam_stat} -U {input.reads_id} -O {output.unmapped_id}"
				)


		rule remove_Unmapped_id:
			input:
				r1 = PROJECT_DIR + "/raw/{samplename}.R1.fq.gz",
				r2 = PROJECT_DIR + "/raw/{samplename}.R2.fq.gz",
				unmapped_id = PROJECT_DIR + "/mapping/{samplename}/Unmapped.id.xls",
			output:
				r1_out = PROJECT_DIR + "/raw_clean/raw/{samplename}.R1.fq.gz",
				r2_out = PROJECT_DIR + "/raw_clean/raw/{samplename}.R2.fq.gz",
			threads:
				softconfig["rule_remove_Unmapped_id"]["threads"]
			params:
				seqkit = softconfig["rule_remove_Unmapped_id"]["soft"]["seqkit"]["path"],
			run:
				os.makedirs(PROJECT_DIR + "/raw_clean/raw") if not os.path.exists(PROJECT_DIR + "/raw_clean/raw") else ""
				shell(
					"{params.seqkit} grep -v -f {input.unmapped_id} {input.r1} -o {output.r1_out}"
				)
				shell(
					"{params.seqkit} grep -v -f {input.unmapped_id} {input.r2} -o {output.r2_out}"
				)


	else:
		
		rule Unmapped_out:
			input:
				mapp = PROJECT_DIR + "/mapping/{samplename}/Aligned.sortedByCoord.ori.bam",
			output:
				unmapped_out = PROJECT_DIR + "/mapping/{samplename}/Unmapped.out.xls",
			threads:
				softconfig["rule_Unmapped_out"]["threads"]
			params:
				samtools = softconfig["rule_Unmapped_out"]["soft"]["samtools"]["path"],
			run:
				shell(
					"{params.samtools} view {input.mapp} | awk '{{if($6==\"*\") print \"@\"$1}}' |sort |uniq > {output.unmapped_out}"
				)


		rule Unmapped_id:
			input:
				bam_stat = PROJECT_DIR + "/supp/mapping/bam_stat.xls",
				reads_id = PROJECT_DIR + "/UID/{samplename}.reads_ids.txt",
				unmapped_out = PROJECT_DIR + "/mapping/{samplename}/Unmapped.out.xls",
			output:
				unmapped_id = PROJECT_DIR + "/mapping/{samplename}/Unmapped.id.xls",
			threads:
				softconfig["rule_Unmapped_id"]["threads"]
			params:
				select_unmapped = softconfig["rule_Unmapped_id"]["soft"]["select_unmapped"]["path"],
				container = softconfig["rule_Unmapped_id"]["singularity"]["py3"]["path"],
				conargs = softconfig["rule_Unmapped_id"]["singularity"]["py3"]["conargs"],
				python3 = softconfig["rule_Unmapped_id"]["singularity"]["py3"]["soft"]["python3"]["cmd"],
				singularity = softconfig["envs"]["singularity"],
			run:
				shell(
					"{params.singularity} {params.conargs} {BIND_DIRS} {params.container} \
                                        {params.python3} {params.select_unmapped}  -N {input.unmapped_out} \
					-B {input.bam_stat} -U {input.reads_id} -O {output.unmapped_id} -S False"
				)


		rule remove_Unmapped_id:
			input:
				r1 = PROJECT_DIR + "/raw/{samplename}.R1.fq.gz",
				r2 = PROJECT_DIR + "/raw/{samplename}.R2.fq.gz",
				unmapped_id = PROJECT_DIR + "/mapping/{samplename}/Unmapped.id.xls",
			output:
				r1_out = PROJECT_DIR + "/raw_clean/raw/{samplename}.R1.fq.gz",
				r2_out = PROJECT_DIR + "/raw_clean/raw/{samplename}.R2.fq.gz",
			threads:
				softconfig["rule_remove_Unmapped_id"]["threads"]
			params:
				seqkit = softconfig["rule_remove_Unmapped_id"]["soft"]["seqkit"]["path"],
			run:
				os.makedirs(PROJECT_DIR + "/raw_clean/raw") if not os.path.exists(PROJECT_DIR + "/raw_clean/raw") else ""
				shell(
					"{params.seqkit} grep -v -f {input.unmapped_id} {input.r1} -o {output.r1_out}"
				)
				shell(
					"{params.seqkit} grep -v -f {input.unmapped_id} {input.r2} -o {output.r2_out}"
				)


else:
	if(ALIGN == "STAR"):

		rule Unmapped_id:
			input:
				unmapped_mate1 = PROJECT_DIR + "/mapping/{samplename}/Unmapped.out.mate1",
				bam_stat = PROJECT_DIR + "/supp/mapping/bam_stat.xls",
			output:
				unmapped_id = PROJECT_DIR + "/mapping/{samplename}/Unmapped.id.xls",
			threads:
				softconfig["rule_Unmapped_id"]["threads"]
			params:
				select_unmapped = softconfig["rule_Unmapped_id"]["soft"]["select_unmapped"]["path"],
				container = softconfig["rule_Unmapped_id"]["singularity"]["py3"]["path"],
				conargs = softconfig["rule_Unmapped_id"]["singularity"]["py3"]["conargs"],
				python3 = softconfig["rule_Unmapped_id"]["singularity"]["py3"]["soft"]["python3"]["cmd"],
				singularity = softconfig["envs"]["singularity"],
			run:
				shell(
					"{params.singularity} {params.conargs} {BIND_DIRS} {params.container} \
                                        {params.python3} {params.select_unmapped} -N {input.unmapped_mate1} \
					-B {input.bam_stat} -O {output.unmapped_id}"
				)


		rule remove_Unmapped_id:
			input:
				r1 = PROJECT_DIR + "/raw/{samplename}.R1.fq.gz",
				r2 = PROJECT_DIR + "/raw/{samplename}.R2.fq.gz",
				unmapped_id = PROJECT_DIR + "/mapping/{samplename}/Unmapped.id.xls",
			output:
				r1_out = PROJECT_DIR + "/raw_clean/raw/{samplename}.R1.fq.gz",
				r2_out = PROJECT_DIR + "/raw_clean/raw/{samplename}.R2.fq.gz",
			threads:
				softconfig["rule_remove_Unmapped_id"]["threads"]
			params:
				seqkit = softconfig["rule_remove_Unmapped_id"]["soft"]["seqkit"]["path"],
			run:
				os.makedirs(PROJECT_DIR + "/raw_clean/raw") if not os.path.exists(PROJECT_DIR + "/raw_clean/raw") else ""
				shell(
					"{params.seqkit} grep -v -f {input.unmapped_id} {input.r1} -o {output.r1_out}"
				)
				shell(
					"{params.seqkit} grep -v -f {input.unmapped_id} {input.r2} -o {output.r2_out}"
				)

	else:

		rule Unmapped_out:
			input:
				mapp = PROJECT_DIR + "/mapping/{samplename}/Aligned.sortedByCoord.ori.bam",
			output:
				unmapped_out = PROJECT_DIR + "/mapping/{samplename}/Unmapped.out.xls",
			threads:
				softconfig["rule_Unmapped_out"]["threads"]
			params:
				samtools = softconfig["rule_Unmapped_out"]["soft"]["samtools"]["path"],
			run:
				shell(
					"{params.samtools} view {input.mapp} | awk '{{if($6==\"*\") print \"@\"$1}}' |sort |uniq > {output.unmapped_out}"
				)


		rule Unmapped_id:
			input:
				unmapped_out = PROJECT_DIR + "/mapping/{samplename}/Unmapped.out.xls",
				bam_stat = PROJECT_DIR + "/supp/mapping/bam_stat.xls",
			output:
				unmapped_id = PROJECT_DIR + "/mapping/{samplename}/Unmapped.id.xls",
			threads:
				softconfig["rule_Unmapped_id"]["threads"]
			params:
				select_unmapped = softconfig["rule_Unmapped_id"]["soft"]["select_unmapped"]["path"],
				container = softconfig["rule_Unmapped_id"]["singularity"]["py3"]["path"],
				conargs = softconfig["rule_Unmapped_id"]["singularity"]["py3"]["conargs"],
				python3 = softconfig["rule_Unmapped_id"]["singularity"]["py3"]["soft"]["python3"]["cmd"],
				singularity = softconfig["envs"]["singularity"],
			run:
				shell(
					"{params.singularity} {params.conargs} {BIND_DIRS} {params.container} \
                                        {params.python3} {params.select_unmapped} -N {input.unmapped_out} \
					-B {input.bam_stat} -O {output.unmapped_id} -S False"
				)


		rule remove_Unmapped_id:
			input:
				r1 = PROJECT_DIR + "/raw/{samplename}.R1.fq.gz",
				r2 = PROJECT_DIR + "/raw/{samplename}.R2.fq.gz",
				unmapped_id = PROJECT_DIR + "/mapping/{samplename}/Unmapped.id.xls",
			output:
				r1_out = PROJECT_DIR + "/raw_clean/raw/{samplename}.R1.fq.gz",
				r2_out = PROJECT_DIR + "/raw_clean/raw/{samplename}.R2.fq.gz",
			threads:
				softconfig["rule_remove_Unmapped_id"]["threads"]
			params:
				seqkit = softconfig["rule_remove_Unmapped_id"]["soft"]["seqkit"]["path"],
			run:
				os.makedirs(PROJECT_DIR + "/raw_clean/raw") if not os.path.exists(PROJECT_DIR + "/raw_clean/raw") else ""
				shell(
					"{params.seqkit} grep -v -f {input.unmapped_id} {input.r1} -o {output.r1_out}"
				)
				shell(
					"{params.seqkit} grep -v -f {input.unmapped_id} {input.r2} -o {output.r2_out}"
				)
