<?php
    $db=new SQLite3('playlist.db');
    $nsig = shell_exec("/data/data/com.termux/files/usr/bin/python2 /data/data/com.termux/files/home/lighttpd/www/playlist.py sig2");
    if ($nsig) {
        $query = $db->exec('DELETE FROM sig');
        $query = $db->exec("INSERT INTO sig (sig,time) VALUES ('".$nsig."', '".time()."')");
        if(!isset($query)) { exit; }
        echo "$nsig";
    } else { exit; }
?>
