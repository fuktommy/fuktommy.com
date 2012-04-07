<?php
    require_once 'ModifireChain.php';
    $chain = ModifireChain::factory();
    $chain->text = 'Hello World. 10 < 11';
    $chain->array = array('a', 'b', 'c');
    $chain->assoc = array('a' => array('b' => 'c'));

    $obj = new StdClass();
    $obj->foo = 'bar';
    $chain->obj = $obj;
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="ja" lang="ja">
<head>
  <meta http-equiv="content-type" content="text/html; charset=UTF-8" />
  <title>ModifireChain Sample</title>
</head>
<body>
<p><?php $chain->text->e(); ?></p>

<ul>
<?php foreach ($chain->array as $k => $v): ?>
  <li><?php $chain->pack($k)->e(); ?>: <?php $v->e(); ?></li>
<?php endforeach; ?>
</ul>

<p><?php $chain->assoc->get('a')->get('b')->e(); ?></p>

<p><?php $chain->obj->foo->e(); ?></p>
</body>
</html>
