A buildout recipe that recursively copies files and directories - useful for syncing eg. django static media.

Based loosely on Alexander Artemenko's symlink recipe at https://github.com/svetlyak40wt/svetlyak40wt.recipe.symlinks

New or changed local files are copied to the destination root path.  Files are never removed from destination.

Files already existing on destination are md5-ed and the hash compared and only changed files are updated.


Sample config:

::
    
    [buildout]
        ...
        find-links = http://github.com/unomena/unomena.recipe.cp/tarball/0.0.1#egg=unomena.recipe.cp-0.0.1
    
    [sync-static]
    recipe = unomena.recipe.cp
    root_path = static
    paths = ${buildout:parts-directory}/django/django/contrib/admin/media admin
            ${buildout:directory}/src/${buildout:app-name}/static/${buildout:app-name}
            django-ckeditor://ckeditor/media/ckeditor
    

