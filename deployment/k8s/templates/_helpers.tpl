
```tpl
{{/*
Expand the name of the chart.
*/}}
{{- define "ontocms-public-hub.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
*/}}
{{- define "ontocms-public-hub.fullname" -}}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "ontocms-public-hub.labels" -}}
helm.sh/chart: {{ include "ontocms-public-hub.chart" . }}
{{ include "ontocms-public-hub.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "ontocms-public-hub.selectorLabels" -}}
app.kubernetes.io/name: {{ include "ontocms-public-hub.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
```