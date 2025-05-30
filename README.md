jmeter 설치하고
bin/system.properties 

```jsx
https.proxyHost=192.168.0.40
https.proxyPort=50000
http.proxyHost=192.168.0.40
http.proxyPort=50000
https.nonProxyHosts=
```

맨아래에 이거추가

실행

```jsx
jmeter -n -t jmeter_https_proxy_test_50.jmx -l result_50.jtl
```