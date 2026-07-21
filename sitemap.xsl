<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:s="http://www.sitemaps.org/schemas/sitemap/0.9">
<xsl:output method="html" encoding="UTF-8" indent="yes"/>
<xsl:template match="/">
<html lang="en"><head><meta charset="UTF-8"/><title>Sitemap · Skill Dev</title>
<style>
body{font:14px/1.5 -apple-system,Segoe UI,Roboto,sans-serif;color:#1a2233;margin:0;background:#f6f8fc}
.wrap{max-width:1100px;margin:0 auto;padding:32px 20px}
h1{color:#0b3d91;font-size:22px;margin:0 0 4px}
.sub{color:#5a6478;margin:0 0 20px}
table{width:100%;border-collapse:collapse;background:#fff;border-radius:8px;overflow:hidden;box-shadow:0 1px 4px rgba(11,61,145,.08)}
th{background:#0b3d91;color:#fff;text-align:left;padding:10px 12px;font-size:12px;text-transform:uppercase;letter-spacing:.04em}
td{border-top:1px solid #e2e7f0;padding:9px 12px;font-size:13px;vertical-align:top}
td a{color:#0b3d91;text-decoration:none}
td a:hover{text-decoration:underline}
tr:nth-child(even) td{background:#f9fbfe}
.pri{font-variant-numeric:tabular-nums;color:#5a6478}
</style></head><body><div class="wrap">
<h1>Skill Dev — Sitemap</h1>
<p class="sub">Total URLs: <xsl:value-of select="count(s:urlset/s:url)"/></p>
<table><thead><tr><th>URL</th><th>Last modified</th><th>Change freq.</th><th>Priority</th></tr></thead>
<tbody>
<xsl:for-each select="s:urlset/s:url">
<tr>
<td><a href="{s:loc}"><xsl:value-of select="s:loc"/></a></td>
<td><xsl:value-of select="s:lastmod"/></td>
<td><xsl:value-of select="s:changefreq"/></td>
<td class="pri"><xsl:value-of select="s:priority"/></td>
</tr>
</xsl:for-each>
</tbody></table>
</div></body></html>
</xsl:template>
</xsl:stylesheet>