#!/usr/bin/env nextflow

nextflow.enable.dsl=2

params.nfeatures = 2000
params.npcs = 30
params.rootparentnode = 'Y_14'

process singlecell {
    script:
    """
    Rscript -e "rmarkdown::render(input='~/SingleCell.Rmd')" ${params.nfeatures} ${params.npcs} ${params.rootparentnode}
    """
}

workflow {
    singlecell()
}
