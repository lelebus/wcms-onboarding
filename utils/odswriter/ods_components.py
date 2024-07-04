from __future__ import unicode_literals

content_xml = """<office:document-content xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" xmlns:calcext="urn:org:documentfoundation:names:experimental:calc:xmlns:calcext:1.0" xmlns:chart="urn:oasis:names:tc:opendocument:xmlns:chart:1.0" xmlns:css3t="http://www.w3.org/TR/css3-text/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dom="http://www.w3.org/2001/xml-events" xmlns:dr3d="urn:oasis:names:tc:opendocument:xmlns:dr3d:1.0" xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0" xmlns:drawooo="http://openoffice.org/2010/draw" xmlns:field="urn:openoffice:names:experimental:ooo-ms-interop:xmlns:field:1.0" xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0" xmlns:form="urn:oasis:names:tc:opendocument:xmlns:form:1.0" xmlns:formx="urn:openoffice:names:experimental:ooxml-odf-interop:xmlns:form:1.0" xmlns:grddl="http://www.w3.org/2003/g/data-view#" xmlns:math="http://www.w3.org/1998/Math/MathML" xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0" xmlns:number="urn:oasis:names:tc:opendocument:xmlns:datastyle:1.0" xmlns:of="urn:oasis:names:tc:opendocument:xmlns:of:1.2" xmlns:ooo="http://openoffice.org/2004/office" xmlns:oooc="http://openoffice.org/2004/calc" xmlns:ooow="http://openoffice.org/2004/writer" xmlns:presentation="urn:oasis:names:tc:opendocument:xmlns:presentation:1.0" xmlns:rpt="http://openoffice.org/2005/report" xmlns:script="urn:oasis:names:tc:opendocument:xmlns:script:1.0" xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0" xmlns:svg="urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0" xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0" xmlns:tableooo="http://openoffice.org/2009/table" xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" xmlns:xforms="http://www.w3.org/2002/xforms" xmlns:xhtml="http://www.w3.org/1999/xhtml" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" office:version="1.2">
    <office:automatic-styles>
        <style:style style:name="ta1" style:family="table">
            <style:table-properties table:display="true" style:writing-mode="lr-tb"/>
        </style:style>
        <style:style style:name="odswriterTime" style:family="table-cell" style:data-style-name="odswriterStyleXMLTime"/>
        <number:date-style style:name="DateISO" number:automatic-order="true">
            <number:year />
            <number:text>-</number:text>
            <number:month number:style="long" />
            <number:text>-</number:text>
            <number:day number:style="long" />
        </number:date-style>
        <number:boolean-style style:name="Bool">
            <number:boolean />
        </number:boolean-style>
        <style:style style:name="cDateISO" style:family="table-cell" style:parent-style-name="Default" style:data-style-name="DateISO" />
        <style:style style:name="cTime" style:family="table-cell" style:parent-style-name="Default" style:data-style-name="Time" />
        <style:style style:name="cBool" style:family="table-cell" style:parent-style-name="Default" style:data-style-name="Bool" />
    </office:automatic-styles>
    <office:body>
        <office:spreadsheet>
        </office:spreadsheet>
    </office:body>
</office:document-content>"""

manifest_rdf = """<?xml version="1.0" encoding="utf-8"?>
<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="styles.xml">
    <rdf:type rdf:resource="http://docs.oasis-open.org/ns/office/1.2/meta/odf#StylesFile"/>
  </rdf:Description>
  <rdf:Description rdf:about="">
    <ns0:hasPart xmlns:ns0="http://docs.oasis-open.org/ns/office/1.2/meta/pkg#" rdf:resource="styles.xml"/>
  </rdf:Description>
  <rdf:Description rdf:about="content.xml">
    <rdf:type rdf:resource="http://docs.oasis-open.org/ns/office/1.2/meta/odf#ContentFile"/>
  </rdf:Description>
  <rdf:Description rdf:about="">
    <ns0:hasPart xmlns:ns0="http://docs.oasis-open.org/ns/office/1.2/meta/pkg#" rdf:resource="content.xml"/>
  </rdf:Description>
  <rdf:Description rdf:about="">
    <rdf:type rdf:resource="http://docs.oasis-open.org/ns/office/1.2/meta/pkg#Document"/>
  </rdf:Description>
</rdf:RDF>"""

mimetype = "application/vnd.oasis.opendocument.spreadsheet"

manifest_xml = """<?xml version="1.0" encoding="UTF-8"?>
<manifest:manifest xmlns:manifest="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0" manifest:version="1.2">
 <manifest:file-entry manifest:full-path="/" manifest:version="1.2" manifest:media-type="application/vnd.oasis.opendocument.spreadsheet"/>
 <manifest:file-entry manifest:full-path="content.xml" manifest:media-type="text/xml"/>
 <manifest:file-entry manifest:full-path="styles.xml" manifest:media-type="text/xml"/>
</manifest:manifest>
"""

styles_xml = """<office:document-styles xmlns:presentation="urn:oasis:names:tc:opendocument:xmlns:presentation:1.0"
    xmlns:css3t="http://www.w3.org/TR/css3-text/" xmlns:rpt="http://openoffice.org/2005/report"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:chart="urn:oasis:names:tc:opendocument:xmlns:chart:1.0"
    xmlns:svg="urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0"
    xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0"
    xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
    xmlns:oooc="http://openoffice.org/2004/calc"
    xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
    xmlns:ooow="http://openoffice.org/2004/writer"
    xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
    xmlns:ooo="http://openoffice.org/2004/office"
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:dr3d="urn:oasis:names:tc:opendocument:xmlns:dr3d:1.0"
    xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0"
    xmlns:number="urn:oasis:names:tc:opendocument:xmlns:datastyle:1.0"
    xmlns:of="urn:oasis:names:tc:opendocument:xmlns:of:1.2"
    xmlns:calcext="urn:org:documentfoundation:names:experimental:calc:xmlns:calcext:1.0"
    xmlns:tableooo="http://openoffice.org/2009/table"
    xmlns:drawooo="http://openoffice.org/2010/draw"
    xmlns:grddl="http://www.w3.org/2003/g/data-view#"
    xmlns:loext="urn:org:documentfoundation:names:experimental:office:xmlns:loext:1.0"
    xmlns:dom="http://www.w3.org/2001/xml-events"
    xmlns:field="urn:openoffice:names:experimental:ooo-ms-interop:xmlns:field:1.0"
    xmlns:math="http://www.w3.org/1998/Math/MathML"
    xmlns:form="urn:oasis:names:tc:opendocument:xmlns:form:1.0"
    xmlns:script="urn:oasis:names:tc:opendocument:xmlns:script:1.0"
    xmlns:xhtml="http://www.w3.org/1999/xhtml" office:version="1.3">
    <office:font-face-decls>
        <style:font-face style:name="Liberation Sans" svg:font-family="'Liberation Sans'"
            style:font-family-generic="swiss" style:font-pitch="variable" />
        <style:font-face style:name="Noto Sans CJK SC" svg:font-family="'Noto Sans CJK SC'"
            style:font-family-generic="system" style:font-pitch="variable" />
        <style:font-face style:name="Noto Sans Devanagari" svg:font-family="'Noto Sans Devanagari'"
            style:font-family-generic="system" style:font-pitch="variable" />
    </office:font-face-decls>
    <office:styles>
        <style:default-style style:family="table-cell">
            <style:paragraph-properties style:tab-stop-distance="1.25cm" />
            <style:text-properties style:font-name="Liberation Sans" fo:font-size="10pt"
                fo:language="it" fo:country="IT" style:font-name-asian="Noto Sans CJK SC"
                style:font-size-asian="10pt" style:language-asian="zh" style:country-asian="CN"
                style:font-name-complex="Noto Sans Devanagari" style:font-size-complex="10pt"
                style:language-complex="hi" style:country-complex="IN" />
        </style:default-style>
        <number:number-style style:name="N0">
            <number:number number:min-integer-digits="1" />
        </number:number-style>
        <style:style style:name="Default" style:family="table-cell" />
        <style:style style:name="Heading" style:family="table-cell"
            style:parent-style-name="Default">
            <style:text-properties fo:color="#000000" fo:font-size="24pt" fo:font-style="normal"
                fo:font-weight="bold" style:font-size-asian="24pt" style:font-style-asian="normal"
                style:font-weight-asian="bold" style:font-size-complex="24pt"
                style:font-style-complex="normal" style:font-weight-complex="bold" />
        </style:style>
        <style:style style:name="Heading_20_1" style:display-name="Heading 1"
            style:family="table-cell" style:parent-style-name="Heading">
            <style:text-properties fo:font-size="18pt" style:font-size-asian="18pt"
                style:font-size-complex="18pt" />
        </style:style>
        <style:style style:name="Heading_20_2" style:display-name="Heading 2"
            style:family="table-cell" style:parent-style-name="Heading">
            <style:text-properties fo:font-size="12pt" style:font-size-asian="12pt"
                style:font-size-complex="12pt" />
        </style:style>
        <style:style style:name="Text" style:family="table-cell" style:parent-style-name="Default" />
        <style:style style:name="Note" style:family="table-cell" style:parent-style-name="Text">
            <style:table-cell-properties fo:background-color="#ffffcc" style:diagonal-bl-tr="none"
                style:diagonal-tl-br="none" fo:border="0.74pt solid #808080" />
            <style:text-properties fo:color="#333333" />
        </style:style>
        <style:style style:name="Footnote" style:family="table-cell" style:parent-style-name="Text">
            <style:text-properties fo:color="#808080" fo:font-style="italic"
                style:font-style-asian="italic" style:font-style-complex="italic" />
        </style:style>
        <style:style style:name="Hyperlink" style:family="table-cell" style:parent-style-name="Text">
            <style:text-properties fo:color="#0000ee" style:text-underline-style="solid"
                style:text-underline-width="auto" style:text-underline-color="#0000ee" />
        </style:style>
        <style:style style:name="Status" style:family="table-cell" style:parent-style-name="Default" />
        <style:style style:name="Good" style:family="table-cell" style:parent-style-name="Status">
            <style:table-cell-properties fo:background-color="#ccffcc" />
            <style:text-properties fo:color="#006600" />
        </style:style>
        <style:style style:name="Neutral" style:family="table-cell" style:parent-style-name="Status">
            <style:table-cell-properties fo:background-color="#ffffcc" />
            <style:text-properties fo:color="#996600" />
        </style:style>
        <style:style style:name="Bad" style:family="table-cell" style:parent-style-name="Status">
            <style:table-cell-properties fo:background-color="#ffcccc" />
            <style:text-properties fo:color="#cc0000" />
        </style:style>
        <style:style style:name="Warning" style:family="table-cell" style:parent-style-name="Status">
            <style:text-properties fo:color="#cc0000" />
        </style:style>
        <style:style style:name="Error" style:family="table-cell" style:parent-style-name="Status">
            <style:table-cell-properties fo:background-color="#cc0000" />
            <style:text-properties fo:color="#ffffff" fo:font-weight="bold"
                style:font-weight-asian="bold" style:font-weight-complex="bold" />
        </style:style>
        <style:style style:name="Accent" style:family="table-cell" style:parent-style-name="Default">
            <style:text-properties fo:font-weight="bold" style:font-weight-asian="bold"
                style:font-weight-complex="bold" />
        </style:style>
        <style:style style:name="Accent_20_1" style:display-name="Accent 1"
            style:family="table-cell" style:parent-style-name="Accent">
            <style:table-cell-properties fo:background-color="#000000" />
            <style:text-properties fo:color="#ffffff" />
        </style:style>
        <style:style style:name="Accent_20_2" style:display-name="Accent 2"
            style:family="table-cell" style:parent-style-name="Accent">
            <style:table-cell-properties fo:background-color="#808080" />
            <style:text-properties fo:color="#ffffff" />
        </style:style>
        <style:style style:name="Accent_20_3" style:display-name="Accent 3"
            style:family="table-cell" style:parent-style-name="Accent">
            <style:table-cell-properties fo:background-color="#dddddd" />
        </style:style>
        <style:style style:name="Result" style:family="table-cell" style:parent-style-name="Default">
            <style:text-properties fo:font-style="italic" style:text-underline-style="solid"
                style:text-underline-width="auto" style:text-underline-color="font-color"
                fo:font-weight="bold" style:font-style-asian="italic" style:font-weight-asian="bold"
                style:font-style-complex="italic" style:font-weight-complex="bold" />
        </style:style>
    </office:styles>
    <office:automatic-styles>
        <style:page-layout style:name="Mpm1">
            <style:page-layout-properties style:writing-mode="lr-tb" />
            <style:header-style>
                <style:header-footer-properties fo:min-height="0.75cm" fo:margin-left="0cm"
                    fo:margin-right="0cm" fo:margin-bottom="0.25cm" />
            </style:header-style>
            <style:footer-style>
                <style:header-footer-properties fo:min-height="0.75cm" fo:margin-left="0cm"
                    fo:margin-right="0cm" fo:margin-top="0.25cm" />
            </style:footer-style>
        </style:page-layout>
    </office:automatic-styles>
    <office:master-styles>
        <style:master-page style:name="Default" style:page-layout-name="Mpm1">
            <style:header>
                <text:p>
                    <text:sheet-name>???</text:sheet-name>
                </text:p>
            </style:header>
            <style:header-left style:display="false" />
            <style:header-first style:display="false" />
            <style:footer>
                <text:p> Page <text:page-number>1</text:page-number>
                </text:p>
            </style:footer>
            <style:footer-left style:display="false" />
            <style:footer-first style:display="false" />
        </style:master-page>
    </office:master-styles>
</office:document-styles>"""
