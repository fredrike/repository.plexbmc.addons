<?php
//https://gist.github.com/619858
// Use in the "Post-Receive URLs" section of your GitHub repo.
//phpinfo();
echo "<pre>";
echo shell_exec( 'cd /opt/data/www/htdocs/repository.plexbmc.addons && \
		/opt/local/bin/git fetch origin && \
		/opt/local/bin/git reset --hard origin && \
		/opt/local/bin/git submodule foreach /opt/local/bin/git remote update && \
		/opt/local/bin/git submodule foreach /opt/local/bin/git merge origin/master && \
		/opt/local/bin/python addons_xml_generator.py' );
echo "<pre>";
//if ( $_POST['payload'] ) {
//  shell_exec( 'cd /opt/data/www/htdocs/repository.plexbmc.addons && git reset --hard HEAD && git pull' );
//}

?>
