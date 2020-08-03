{
  service:: {
    new(name, namespace, app, ports): {
      apiVersion: 'v1',
      kind: 'Service',
      metadata: {
        labels: {
          app: app,
          env: namespace,
        },
        name: name,
        namespace: namespace,
      },
      spec: {
        type: 'NodePort',
        selector: {
          app: app,
          env: namespace,
        },
        ports: ports,
      },
    },
  },
}
