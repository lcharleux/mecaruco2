import sys, os, shutil
from string import Template
import subprocess
sys.path.append(os.path.abspath('sphinxext'))

################################################################################
# NOTEBOOKS MANAGEMENT
################################################################################
# SETUP
nbdir  = "./notebooks/"     # The notebooks that contains the notebooks.
rstdir = "./notebooks_rst/" # The directory where sphinx can store rst files.
template = Template(open("notebooks_index.template").read())
exclude_prefixes = ('_', '.')  # exclusion prefixes for files and folders
title_levels = "+=~-_"


nbdir = nbdir.strip("./")
rstdir = rstdir.strip("./")

# DATA PROCESSING (whole section needs serious cleaning)
for dirpath, dirnames, filenames in os.walk(nbdir):
    dirnames[:] = sorted([dirname for dirname in dirnames
                   if not dirname.startswith(exclude_prefixes)])
    filenames[:] = sorted([f for f in filenames 
                   if True not in [f.startswith(ep) for ep 
                                   in exclude_prefixes]])
    print("DIR PATH: ", dirpath)
    print("  DIR NAMES: ", dirnames)
    print("  DIR FILENAMES: ", filenames)
    
    # PATH MANAGEMENT
    dirpath = dirpath.strip("./")
    pathdepth = len(dirpath.strip("/").split("/")) 
    rstpath   = dirpath.replace(nbdir, rstdir).strip("/").strip("./") + "/"
    rootpath  = "/".join([".."] * pathdepth) + "/"
    if os.path.isdir(rstpath) == False: 
        os.mkdir(rstpath)
    node = dirpath.strip("/").split("/")[-1]
    
    # TITLE
    nodetitle = node.split("_")
    if len(nodetitle) > 1: 
        nodetitle = " ".join(nodetitle[1:])
    else:
        nodetitle = nodetitle[0] 
    print("  TITLE: ", nodetitle) 
    otherfiles = []
    notebooks  = []
    
    for f in filenames:
        if f.endswith(".ipynb"): # NOTEBOOKS
            # NOTEBOOK NAME
            nb = f[:-6]
            notebooks.append(nb)
            # RST CONVERSION
            nbrstpath = rstpath + nb +".rst" # WARNING: NBCONVERT WORKS IN NOTEBOOK DIR, NOT IN CURRENT DIR
            rstconvertcommand = "jupyter-nbconvert {0}/{1}.ipynb --to rst --output {2}"
            os.system(rstconvertcommand.format(dirpath, nb, rootpath + nbrstpath))
            rst  = ".. Note::\n\n  This notebook can be downloaded here: "
            rst += ":download:`{2}.ipynb <{0}{1}/{2}.ipynb>` \n\n".format(
                     rootpath, dirpath, nb)
            rst += open(nbrstpath).read()
            open(nbrstpath, "w").write(rst)
            
          
        else: # OTHER FILES
            otherfiles.append(f)
    downloadtemplate = "#. :download:`{0}<{1}>`"
    files = ""
    if len(otherfiles)!= 0:
        files = "Files in this folder:\n\n" 
        downloadlinks = [
            downloadtemplate.format(f, rootpath + dirpath + "/" + f) 
            for f in otherfiles ]
        files += "\n".join(downloadlinks)                       
    
    nodeindex = template.substitute(
                         title = nodetitle.title(), 
                         underline = 80 * title_levels[pathdepth],
                         files = files)      
    nodeindex += "\n".join(["   " + nb for nb in notebooks]) 
    for d in dirnames: nodeindex += "   " + d + "/" + d + "\n"
    open(rstpath + node + ".rst", "w").write(nodeindex)
                 
                       
################################################################################


# -- General configuration -----------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be extensions
# coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = ['sphinx.ext.autodoc', 
'sphinx.ext.mathjax',
'sphinx.ext.viewcode',
'sphinx.ext.doctest',
'matplotlib.sphinxext.only_directives',
'matplotlib.sphinxext.plot_directive',
#'sphinx_gallery.gen_gallery'
]

"""
# LC 2018/01/26
# SPHINX GALLERY CONFIG
sphinx_gallery_conf = {
# path to your examples scripts
'examples_dirs' : 'examples',
# path where to save gallery generated examples
'gallery_dirs'  : 'auto_examples',
'backreferences_dir': False}
"""

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The encoding of source files.
source_encoding = 'utf-8-sig'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u"Scientific Python: a collection of science oriented python examples"
copyright = u'2018, Ludovic Charleux, Emile Roux'
show_authors = True

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = '0.0'
# The full version, including alpha/beta/rc tags.
#release = '1.0.0'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
language = 'en_US'

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
#today = ''
# Else, today_fmt is used as the format for a strftime call.
#today_fmt = '%B %d, %Y'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['_build']

# The reST default role (used for this markup: `text`) to use for all documents.
#default_role = None

# If true, '()' will be appended to :func: etc. cross-reference text.
#add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
#add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
show_authors = True

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# A list of ignored prefixes for module index sorting.
#modindex_common_prefix = []


# -- Options for HTML output ---------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#html_theme = 'default'
html_theme = 'sphinx_rtd_theme'

#html_output_encoding = 'iso-8859-1'
html_output_encoding = 'utf-8'


# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#html_theme_options = {'stickysidebar': True, 'sidebarwidth': 250}

# Add any paths that contain custom themes here, relative to this directory.
#html_theme_path = []

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
#html_title = None

# A shorter title for the navigation bar.  Default is the same as html_title.
#html_short_title = None

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
#html_logo = None

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
#html_favicon = None

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
#html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
#html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
#html_sidebars = {}

# Additional templates that should be rendered to pages, maps page names to
# template names.
#html_additional_pages = {}

# If false, no module index is generated.
#html_domain_indices = True

# If false, no index is generated.
#html_use_index = True

# If true, the index is split into individual pages for each letter.
#html_split_index = False

# If true, links to the reST sources are added to the pages.
#html_show_sourcelink = True

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
#html_show_sphinx = True

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
html_show_copyright = False

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
#html_use_opensearch = ''

# This is the file name suffix for HTML files (e.g. ".xhtml").
#html_file_suffix = None

# Output file base name for HTML help builder.
htmlhelp_basename = u'Scientific Python'
html_copy_source = True
html_show_sourcelink = True

