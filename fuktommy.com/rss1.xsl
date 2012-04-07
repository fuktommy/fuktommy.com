<?xml version="1.0" encoding="euc-jp"?>
<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
  xmlns="http://www.w3.org/1999/xhtml"
  xmlns:rss="http://purl.org/rss/1.0/"
  xmlns:dc="http://purl.org/dc/elements/1.1/"
  xmlns:foaf="http://xmlns.com/foaf/0.1/"
  exclude-result-prefixes="rdf rss dc foaf"
>

<xsl:template match="/">
  <xsl:apply-templates select="rdf:RDF"/>
</xsl:template>

<xsl:template match="rdf:RDF">
  <html xml:lang="ja">
    <head>
      <title><xsl:value-of select="rss:channel/rss:title"/></title>
      <link rel="stylesheet" href="/common.css" type="text/css" />
    </head>
    <body>
      <h1><a href="{rss:channel/rss:link}"><xsl:value-of select="rss:channel/rss:title"/></a></h1>
      <p><xsl:value-of select="rss:channel/rss:description"/></p>
      <dl>
        <xsl:apply-templates select="rss:item"/>
      </dl>
    </body>
  </html>
</xsl:template>

<xsl:template match="rss:item">
  <dt><a href="{rss:link}"><xsl:value-of select="rss:title"/></a></dt>
  <dd><xsl:value-of select="dc:date"/></dd>
  <dd><xsl:value-of select="rss:description"/></dd>
</xsl:template>

</xsl:stylesheet>
