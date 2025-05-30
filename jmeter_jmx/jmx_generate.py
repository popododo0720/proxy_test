from datetime import datetime

proxy_host = "192.168.0.40"
proxy_port = "50000"
concurrents = [50, 100, 200, 500]

def generate_jmx(concurrent_users):
    test_plan_name = f"jmeter_https_proxy_test_{concurrent_users}.jmx"
    jmx_template = f"""<?xml version="1.0" encoding="UTF-8"?>
<jmeterTestPlan version="1.2" properties="5.0" jmeter="5.6.3">
  <hashTree>
    <TestPlan guiclass="TestPlanGui" testclass="TestPlan" testname="HTTPS Proxy Load Test ({concurrent_users} users)" enabled="true">
      <stringProp name="TestPlan.comments"></stringProp>
      <boolProp name="TestPlan.functional_mode">false</boolProp>
      <elementProp name="TestPlan.user_defined_variables" elementType="Arguments">
        <collectionProp name="Arguments.arguments">
          <elementProp name="https.proxyHost" elementType="Argument">
            <stringProp name="Argument.value">{proxy_host}</stringProp>
            <stringProp name="Argument.metadata">=</stringProp>
          </elementProp>
          <elementProp name="https.proxyPort" elementType="Argument">
            <stringProp name="Argument.value">{proxy_port}</stringProp>
            <stringProp name="Argument.metadata">=</stringProp>
          </elementProp>
        </collectionProp>
      </elementProp>
    </TestPlan>
    <hashTree>
      <ThreadGroup guiclass="ThreadGroupGui" testclass="ThreadGroup" testname="Thread Group" enabled="true">
        <stringProp name="ThreadGroup.num_threads">{concurrent_users}</stringProp>
        <stringProp name="ThreadGroup.ramp_time">1</stringProp>
        <elementProp name="ThreadGroup.main_controller" elementType="LoopController">
          <boolProp name="LoopController.continue_forever">false</boolProp>
          <stringProp name="LoopController.loops">1</stringProp>
        </elementProp>
      </ThreadGroup>
      <hashTree>
        <HTTPSamplerProxy guiclass="HttpTestSampleGui" testclass="HTTPSamplerProxy" testname="HTTPS Request" enabled="true">
          <stringProp name="HTTPSampler.domain">httpbin.org</stringProp>
          <stringProp name="HTTPSampler.port">443</stringProp>
          <stringProp name="HTTPSampler.protocol">https</stringProp>
          <stringProp name="HTTPSampler.path">/get</stringProp>
          <stringProp name="HTTPSampler.method">GET</stringProp>
        </HTTPSamplerProxy>
        <hashTree/>
      </hashTree>
    </hashTree>
  </hashTree>
</jmeterTestPlan>
"""
    with open(test_plan_name, "w", encoding="utf-8") as f:
        f.write(jmx_template)
    print(f"[+] Generated: {test_plan_name}")

for c in concurrents:
    generate_jmx(c)
