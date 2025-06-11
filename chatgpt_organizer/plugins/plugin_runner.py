import importlib
def run_plugins(plugin_list, *args):
    print(f"[runner] Running plugins: {plugin_list}")
    for plugin in plugin_list:
        try:
            module = importlib.import_module(f"plugins.{plugin}")
            module.run(*args)
        except Exception as e:
            print(f"[runner] Error in {plugin}: {e}")
