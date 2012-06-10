<?xml version="1.0" encoding="UTF-8" ?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output method="html" version="1.0" encoding="UTF-8" indent="yes"/>
  <xsl:template match="/">
    <html xmlns="http://www.w3.org/1999/xhtml">
      <head>
        <title>Rapport <xsl:value-of select="/player/tour"/> du commandant <xsl:value-of select="/player/name"/></title>
        <link rel="stylesheet" href="rapport.css" type="text/css" />
      </head> 
      <body onload=""><center>
        <table class="t1">
            <tr><th colspan="2">Info générales</th></tr>
            <tr><td>(id)</td><td><xsl:value-of select="player/@id"/></td></tr>
            <tr><td>Nom</td><td><xsl:value-of select="player/name"/></td></tr>
            <tr><td>Nom de domaine</td><td><xsl:value-of select="player/domain"/></td></tr>
            <tr><td>Race</td><td><xsl:value-of select="player/race"/></td></tr>
            <tr><td>Numéro du tour</td><td><xsl:value-of select="player/tour"/></td></tr>
            <xsl:for-each select="player/bank">
            <tr><td><xsl:value-of select="@type"/></td><td><xsl:value-of select="."/></td></tr>
            </xsl:for-each>
            <xsl:for-each select="player/percent">
            <tr><td><xsl:value-of select="@type"/></td><td><xsl:value-of select="."/></td></tr>
            </xsl:for-each>
            <xsl:for-each select="player/budget">
            <tr><td><xsl:value-of select="@type"/></td><td><xsl:value-of select="."/></td></tr>
            </xsl:for-each>
        </table>
        
        <xsl:for-each select="player/assets/asset">
            <table><tr><td style="padding: 15px" valign="top">
                <table class="t1">
                    <tr><th colspan="2">Asset <xsl:value-of select="name"/></th></tr>
                    <tr><td>(id)</td><td><xsl:value-of select="@id"/></td></tr>
                    <tr><td>position</td><td>(<xsl:value-of select="position/@x"/>, <xsl:value-of select="position/@y"/>)</td></tr>
                    <tr><td>politique</td><td><xsl:value-of select="policy"/></td></tr>
                    <tr><td>culture</td><td><xsl:value-of select="culture"/></td></tr>
                    <tr><td>PdC</td><td><xsl:value-of select="poc"/></td></tr>
                    <tr><td>Stock Minerai</td><td><xsl:value-of select="ore"/></td></tr>
                </table>
                <table class="t1">
                    <tr><th colspan="2">Poste Commercial</th></tr>
                    <xsl:for-each select="stock_march">
                        <tr><td><xsl:value-of select="@type"/></td><td><xsl:value-of select="."/></td></tr>
                    </xsl:for-each>
                </table>
            </td><td style="padding: 15px">
            <table class="t2">
                <tr><th>id #</th><th>Caracs</th><th>Atmos</th><th>Size</th><th>March</th>
                <th>taxe</th><th>stab</th><th>revolt</th><th>terra</th><th>struct</th><th>minerai</th></tr>
                <xsl:for-each select="planets/planet">
                <tr><td rowspan="3" class="bot"><xsl:value-of select="@id"/> #<xsl:value-of select="position"/></td>
                    <td>T:<xsl:value-of select="caracs/@temp"/> R:<xsl:value-of select="caracs/@rad"/></td>
                    <td><xsl:value-of select="atmosphere"/></td>
                    <td><xsl:value-of select="size"/></td>
                    <td><xsl:value-of select="march"/></td>
                    <td><xsl:value-of select="taxe"/></td>
                    <td><xsl:value-of select="stab"/></td>
                    <td><xsl:value-of select="revolt"/></td>
                    <td><xsl:value-of select="terra"/></td>
                    <td><xsl:value-of select="struct/@max"/></td>
                    <td><xsl:value-of select="ore/@prod"/>/<xsl:value-of select="ore"/></td>
                </tr>
                <tr>
                    <td colspan="10">
                        <xsl:for-each select="pop">
                            <xsl:value-of select="@race"/>: <xsl:value-of select="."/>/<xsl:value-of select="@max"/> 
                            <xsl:if test="@growth">(<xsl:value-of select="@growth"/>%)</xsl:if>   
                        </xsl:for-each>
                    </td>
                </tr>
                <tr>
                    <td colspan="10" class="bot">
                        <xsl:for-each select="building">
                            <xsl:value-of select="@type"/>: <xsl:value-of select="."/>  
                        </xsl:for-each>
                    </td>
                </tr>
                </xsl:for-each>
         </table></td></tr></table>
        </xsl:for-each>
        
            <table class="t1">
                <tr><th>name (id)</th><th>position</th><th>caracs</th><th>compos</th><th>cargo</th></tr>
                <xsl:for-each select="player/fleets/fleet">
                <tr><td><xsl:value-of select="name"/> (<xsl:value-of select="@id"/>)</td>
                    <td><xsl:value-of select="position"/>
                        <xsl:if test="dest"><br/>dest : <xsl:value-of select="dest"/></xsl:if></td>
                    <td>
                        <xsl:for-each select="carac">
                            <xsl:value-of select="@name"/> : <xsl:value-of select="."/><br/>
                        </xsl:for-each>
                    </td>
                    <td>
                        <xsl:for-each select="squad">
                            <xsl:value-of select="@type"/> : <xsl:value-of select="."/> (<xsl:value-of select="@race"/>)<br/>
                        </xsl:for-each>
                    </td><td></td></tr>
                </xsl:for-each>
         </table>
         
         <table class="t1">
                <tr><th>name (id)</th><th>caracs</th><th>marchs</th><th>parents</th></tr>
                <xsl:for-each select="player/technos/techno">
                <tr><td><xsl:value-of select="name"/> (<xsl:value-of select="@id"/>)</td>
                    <td>
                        <xsl:for-each select="carac">
                            <xsl:if test="not(@march)">
                                <xsl:value-of select="@name"/> : <xsl:value-of select="."/><br/>
                            </xsl:if>
                        </xsl:for-each>
                    </td>
                    <td>
                        <xsl:for-each select="carac">
                            <xsl:if test="@march">
                                <xsl:value-of select="@name"/> : <xsl:value-of select="."/>.<xsl:value-of select="@march"/><br/>
                            </xsl:if>
                        </xsl:for-each>
                    </td>
                    <td>
                        <xsl:for-each select="parent">
                            <xsl:value-of select="//techno[@id=current()]/name"/><br/>
                        </xsl:for-each>
                    </td></tr>
                </xsl:for-each>
         </table>
        
         <table class="t1">
                <tr><th>name (id)</th><th>caracs</th><th>marchs</th><th>parents</th></tr>
                <xsl:for-each select="player/ftechnos/techno">
                <tr><td><xsl:value-of select="name"/> (<xsl:value-of select="@id"/>)</td>
                    <td>
                        <xsl:for-each select="carac">
                            <xsl:if test="not(@march)">
                                <xsl:value-of select="@name"/> : <xsl:value-of select="."/><br/>
                            </xsl:if>
                        </xsl:for-each>
                    </td>
                    <td>
                        <xsl:for-each select="carac">
                            <xsl:if test="@march">
                                <xsl:value-of select="@name"/> : <xsl:value-of select="."/>.<xsl:value-of select="@march"/><br/>
                            </xsl:if>
                        </xsl:for-each>
                    </td>
                    <td>
                        <xsl:for-each select="parent">
                            <xsl:value-of select="//techno[@id=current()]/name"/><br/>
                        </xsl:for-each>
                    </td></tr>
                </xsl:for-each>
         </table>
         
         <table class="t1">
                <tr><th>name (id)</th><th>brand</th><th>domain</th><th>caracs</th><th>compos</th><th>marchs</th></tr>
                <xsl:for-each select="player/schemes/ship">
                <tr><td><xsl:value-of select="name"/> (<xsl:value-of select="@id"/>)</td>
                    <td><xsl:value-of select="brand"/></td>
                    <td><xsl:value-of select="domain"/></td>
                    <td>
                        <xsl:for-each select="carac">
                            <xsl:value-of select="@name"/> : <xsl:value-of select="."/><br/>
                        </xsl:for-each>
                    </td>
                    <td>
                        <xsl:for-each select="compo">
                            <xsl:value-of select="@name"/> : <xsl:value-of select="."/><br/>
                        </xsl:for-each>
                    </td>
                    <td>
                        <xsl:for-each select="march">
                            <xsl:value-of select="@name"/> : <xsl:value-of select="."/><br/>
                        </xsl:for-each>
                    </td></tr>
                </xsl:for-each>
         </table><br/><br/>
         <xsl:for-each select="/player/msgs/msg">
            <xsl:value-of select="."/><br/>
         </xsl:for-each>
      </center></body>
    </html>
  </xsl:template>
</xsl:stylesheet>
