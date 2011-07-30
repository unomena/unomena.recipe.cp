import os
import logging
import hashlib
import shutil

import zc.buildout
from zc.recipe.egg import Egg


class CP(Egg):
    """
    Credit to Alexander Artemenko for code borrowed from his symlink recipe:
    https://github.com/svetlyak40wt/svetlyak40wt.recipe.symlinks
    """

    def __init__(self, buildout, name, options):
        self.logger = logging.getLogger(name)
        
        super(CP, self).__init__(buildout, name, options)
        
        # optional parameters
        self.root_path = self.options.get('root_path', '')
        self.paths = [path for path in self.options['paths'].split('\n') if path]
        

    def install(self):
        self._sync_files()
        # we don't want buildout to delete files when uninstalling, so return empty
        return []


    def update(self):
        self._sync_files()


    def _get_resource_filename(self, uri):
        self.logger.info('getting resource filename for uri "%s"' % uri)

        package, path = uri.split('://', 1)

        self.options['eggs'] = package
        ws = self.working_set()[1]
        distributions = ws.require(package)

        if not distributions:
            raise RuntimeError('Can\'t find package "%"' % package)

        package = distributions[0]

        result = os.path.join(package.location, path)
        self.logger.info('resource filename for uri "%s" is "%s"' % (uri, result))
        return result
    
    
    def _sync_files(self):
        # iterate through the paths and upload each
        for path in self.paths:
            parts = path.split(None, 1)
            if len(parts) == 2:
                source, dest = parts
            else:
                source = parts[0]
                dest = os.path.basename(path)

            if '://' in source:
                source = self._get_resource_filename(source)

            # traverse the path and sync each file
            for dirname, dirnames, filenames in os.walk(source):
                for filename in filenames:
                    # get the fqn of the source file
                    source_fqn = os.path.join(dirname, filename)
                    
                    # construct the destination file name
                    dest_fqn = os.path.join(self.root_path, dirname.replace(source, dest), filename)
                    
                    # ensure the destination directory exists
                    if not os.path.exists(os.path.dirname(dest_fqn)):
                        os.makedirs(os.path.dirname(dest_fqn))

                    if os.path.exists(dest_fqn):
                        # determine if we need to update the file
                        md5_source = hashlib.md5(file(source_fqn).read())
                        md5_dest = hashlib.md5(file(dest_fqn).read())
                        
                        if md5_source.hexdigest() == md5_dest.hexdigest():
                            self.logger.info('skipped: %s' % source_fqn)
                            continue
                        else:
                            self.logger.info('files differ: %s' % (source_fqn,))
                        
                    shutil.copy(source_fqn, dest_fqn)
                    self.logger.info('uploaded %s to %s' % (source_fqn, dest_fqn))


