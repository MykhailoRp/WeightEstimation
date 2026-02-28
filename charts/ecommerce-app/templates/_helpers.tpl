{{- define "ecommerce-app.name" -}}
{{ .Chart.Name }}
{{- end }}

{{- define "ecommerce-app.fullname" -}}
{{ .Release.Name }}-{{ .Chart.Name }}
{{- end }}
