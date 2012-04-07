{* -*- coding: utf-8 -*- *}
{* Copyright (c) 2007 Satoshi Fukutomi <info@fuktommy.com>. *}
<?xml version="1.0" encoding="{$rss->encode}"?>
{if $rss->xsl}
<?xml-stylesheet href="{$rss->xsl}" type="text/xsl"?>
{/if}
<rdf:RDF
  xmlns="http://purl.org/rss/1.0/"
  xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
  xmlns:dc="http://purl.org/dc/elements/1.1/"
  xmlns:content="http://purl.org/rss/1.0/modules/content/"
  xml:lang="{$rss->lang}">
<channel rdf:about="{$rss->uri}">
<title>{$rss->title|escape:"html"}</title>
<link>{$rss->link}</link>
<description>{$rss->description|escape:"html"}</description>
<items><rdf:Seq>
{foreach from=$items item="item"}
  <rdf:li rdf:resource="{$item.link}"/>
{/foreach}
</rdf:Seq></items>
</channel>
{foreach from=$items item="item"}
  <item rdf:about="{$item.link}">
  <title>{$item.title}</title>
  <link>{$item.link}</link>
  <dc:date>{$item.date|date_format:"%Y-%m-%dT%H:%M:%SZ"}</dc:date>
  {if $item.creator}
  <dc:creator>f.creator</dc:creator>
  {/if}
  {foreach from=$item.subject item="sub"}
  <dc:subject>{$sub|escape:"html"}</dc:subject>
  {/foreach}
  {if $item.description}
  <description>{$item.description}</description>
  {/if}
  {if $item.content}
    <content:encoded><![CDATA[{$item.content}]]></content:encoded>
  {/if}
  </item>
{/foreach}
</rdf:RDF>
