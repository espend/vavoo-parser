<?php
    if(isset($_GET['id'])) {
        $id=$_GET['id'];
        $db=new SQLite3('playlist.db');
        $res = $db->query('SELECT time FROM sig');
        $row = $res->fetchArray();
        $stime = $row['time'];
        $now = time();
        if($now > $stime + 300) {
            $nsig = shell_exec("/data/data/com.termux/files/usr/bin/python2 /data/data/com.termux/files/home/lighttpd/www/playlist.py sig2");
            if ($nsig) {
                $query = $db->exec('DELETE FROM sig');
                $query = $db->exec("INSERT INTO sig (sig,time) VALUES ('".$nsig."', '".time()."')");
                if(!isset($query)) { exit; }
                $sig = $nsig;
            } else { exit; }
        } else {
            $res = $db->query('SELECT sig FROM sig');
            $row = $res->fetchArray();
            $sig = $row['sig'];
        }

        $test = $db->querySingle('SELECT * FROM channel WHERE id='.$id);
        if(isset($test)) {
            $res = $db->query('SELECT * FROM channel WHERE id='.$id);
            $row = $res->fetchArray();
            $url = $row['url'];

            header("User-Agent: VAVOO/2.6");
            header("Accept: */*");
            header("Access-Control-Allow-Origin: *");
            header("Content-Type: text/plain; charset=utf-8");
            header("Location: {$url}?n=1&b=5&vavoo_auth={$sig}");
        }
        $db->close();
        exit;
    }
?>
