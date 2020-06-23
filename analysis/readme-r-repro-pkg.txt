The following was used to generate r-repro-pkg-list.csv.

CRAN Task View: Reproducible Research
Maintainer:	John Blischak, Alison Hill
Contact:	jdblischak at gmail.com
Version:	2020-04-27
URL:	https://CRAN.R-project.org/view=ReproducibleResearch
The goal of reproducible research is to tie specific instructions to data analysis and experimental data so that scholarship can be recreated, better understood and verified. Packages in R for this purpose can be split into groups for: literate programming, pipeline toolkits, package reproducibility, project workflows, code/data formatting tools, format convertors, and object caching.

The maintainers gratefully acknowledge Anna Krystalli , Max Kuhn , Will Landau , Ben Marwick , and Daniel Nüst for their useful feedback and contributions.

Literate Programming

The primary way that R facilitates reproducible research is using a document that is a combination of content and data analysis code. The Sweave function (in the base R utils package) and the knitr package can be used to blend the subject matter and R code so that a single document defines the content and the analysis. The brew and R.rsp packages contain alternative approaches to embedding R code into various markups.

The resources for literate programming are best organized by the document type/markup language:

LaTeX

Both Sweave and knitr can process LaTeX files. lazyWeave can create LaTeX documents from scratch.

Object Conversion Functions:

summary tables/statistics : Hmisc, NMOF, papeR, quantreg, rapport, reporttools, sparktex, tables, xtable, ztable
tables/cross-tabulations : Hmisc, lazyWeave, knitLatex, knitr, reporttools, ztable
graphics : animation, Hmisc, grDevices:::pictex, sparktex, tikzDevice
statistical models/methods : apsrtable, memisc, quantreg, rms, stargazer, suRtex, texreg, xtable, ztable
bibtex : bibtex and RefManageR
others : latex2exp converts LaTeX equations to plotmath expressions.
Miscellaneous Tools

Hmisc contains a function to correctly escape special characters. resumer creates resumes. Standardized exams can be created using the exams package.
HTML
The knitr package can process HTML files directly. Sweave can also work with HTML by way of the R2HTML package. lazyWeave can create HTML format documents from scratch.

Object Conversion Functions:

summary tables/statistics : stargazer
tables/cross-tabulations : DT, formattable, htmlTable, HTMLUtils, hwriter, knitr, lazyWeave, SortableHTMLTables, texreg, ztable
statistical models/methods : rapport, stargazer, xtable
others : knitcitations, RefManageR
Miscellaneous Tools: htmltools has various tools for working with HTML. tufterhandout for creating Tufte-style handouts

Markdown
The knitr package can process markdown files without assistance. The packages markdown and rmarkdown have general tools for working with documents in this format. lazyWeave can create markdown format documents from scratch.

Object Conversion Functions:

summary tables/statistics : papeR
tables/cross-tabulations : DT, formattable, htmlTable, knitr, lazyWeave, papeR
statistical models/methods : pander, papeR, rapport, texreg
others : RefManageR
Miscellaneous Tools: tufterhandout for creating Tufte-style handouts. kfigr allows for figure indexing in markdown documents.

OpenDocument Format (ODF)
Object Conversion Functions:

statistical models/methods : rapport
Microsoft Formats
R2wd (windows only) can also create Word documents from scratch and R2PPT (also windows only) can create PowerPoint slides. The rtf package does the same for Rich Text Format documents.

Pipeline Toolkits
Pipeline toolkits help maintain and verify reproducibility. They synchronize computational output with the underlying code and data, and they tell the user when everything is up to date. In other words, they provide concrete evidence that results are re-creatable from the starting materials, and the data analysis project does not need to rerun from scratch. The drake package is such a pipeline toolkit. It is similar to GNU Make , but it is R-focused.

drake: A general-purpose computational engine for data analysis, drake rebuilds intermediate data objects when their dependencies change, and it skips work when the results are already up to date.
repo: A data manager meant to avoid manual storage/retrieval of data to/from the file system.
Package Reproducibility
R also has tools for ensuring that specific packages versions can be required for analyses. checkpoint, rbundler, packrat and renv install packages required for a project to a local archive as they existed at a specified point in time. This allows specific package versions to be maintained over time and different users. The miniCRAN package facilitates the creation of local CRAN-like repositories.

Project Workflows
Successfully completing a data analysis project often requires much more than statistics and visualizations. Efficiently managing the code, data, and results as the project matures helps reduce stress and errors. The following "workflow" packages assist the R programmer by managing project infrastructure and/or facilitating a reproducible workflow.

Workflow utility packages provide single-use functions to implement project infrastructure or solve a specific problem. As a typical example, usethis::use_git() initializes a Git repository, ignores common R files, and commits all project files.

cabinets: Creates project specific directory and file templates that are written to a .Rprofile file.
here: Constructs paths to your project's files.
prodigenr: Create a project directory structure, along with typical files for that project.
RepoGenerator: Generates a project and repo for easy initialization of a GitHub repo for R workshops.
rrtools ( GitHub only ): Instructions, templates, and functions for making a basic compendium suitable for doing reproducible research with R.
starters ( GitHub only ): Setting up R project directories for teaching, presenting, analysis, package development can be a pain. starters shortcuts this by creating folder structures and setting good defaults for you.
usethis: Automate package and project setup tasks that are otherwise performed manually.
Workflow framework packages provide an organized directory structure and helper functions to assist during the development of the project. As a typical example, ProjectTemplate::create.project() creates an organized setup with many subdirectories, and ProjectTemplate::run.project() executes each R script that is saved in the src/ subdirectory.

adapr: Tracks reading and writing within R scripts that are organized into a directed acyclic graph.
exreport: Analysis of experimental results and automatic report generation in both interactive HTML and LaTeX.
madrat: Provides a framework which should improve reproducibility and transparency in data processing. It provides functionality such as automatic meta data creation and management, rudimentary quality management, data caching, work-flow management and data aggregation.
makeProject: This package creates an empty framework of files and directories for the "Load, Clean, Func, Do" structure described by Josh Reich.
orderly: Order, create and store reports from R.
projects: Provides a project infrastructure with a focus on manuscript creation.
ProjectTemplate: Provides functions to automatically build a directory structure for a new R project. Using this structure, 'ProjectTemplate' automates data loading, preprocessing, library importing and unit testing.
represtools: Reproducible research tools automates the creation of an analysis directory structure and work flow. There are R markdown skeletons which encapsulate typical analytic work flow steps. Functions will create appropriate modules which may pass data from one step to another.
RSuite: Supports safe and reproducible solutions development in R. It will help you with environment separation per project, dependency management, local packages creation and preparing deployment packs for your solutions.
tinyProject: Creates useful files and folders for data analysis projects and provides functions to manage data, scripts and output files.
workflowr: Provides a workflow for your analysis projects by combining literate programming ('knitr' and 'rmarkdown') and version control ('Git', via 'git2r') to generate a website containing time-stamped, versioned, and documented results.
Formatting Tools
formatR, highlight, and highr can be used to color and/or format R code.

Packages humanFormat, lubridate, prettyunits, and rprintf have functions to better format data.

Format Convertors
pander can be used for rendering R objects into Pandoc's markdown. knitr has the function pandoc that can call an installed version of Pandoc to convert documents between formats such as Markdown, HTML, LaTeX, PDF and Word.

Object Caching Packages
When using Sweave and knitr it can be advantageous to cache the results of time consuming code chunks if the document will be re-processed (i.e. during debugging). knitr facilitates object caching and the Bioconductor package weaver can be used with Sweave.

Non-literate programming packages to facilitating caching/archiving are R.cache, archivist, and storr.

CRAN packages:
adapr
animation
apsrtable
archivist
bibtex
brew
cabinets
checkpoint
drake
DT
exams
exreport
formatR
formattable
here
highlight
highr
Hmisc (core)
htmlTable
htmltools
HTMLUtils
humanFormat
hwriter
kfigr
knitcitations
knitLatex
knitr (core)
latex2exp
lazyWeave
lubridate
madrat
makeProject
markdown
memisc
miniCRAN
NMOF
orderly
packrat
pander
papeR
prettyunits
prodigenr
projects
ProjectTemplate
quantreg
R.cache
R.rsp
R2HTML (core)
R2PPT
R2wd
rapport
rbundler
RefManageR
renv
repo
RepoGenerator
reporttools
represtools
resumer
rmarkdown
rms (core)
rprintf
RSuite
rtf
SortableHTMLTables
sparktex
stargazer
storr
suRtex
tables
texreg
tikzDevice
tinyProject
tufterhandout
usethis
workflowr
xtable (core)
ztable
