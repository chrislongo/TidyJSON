import json
import re
import sublime
import sublime_plugin


class TidyJsonCommand(sublime_plugin.TextCommand):
    def load_settings(self):
        self.settings = {}

        settings = sublime.load_settings(__name__ + '.sublime-settings')

        for setting in ['indent_width',
                        'item_seperator',
                        'dictionary_seperator',
                        'sort_keys',
                        'compact']:

            self.settings[setting] = settings.get(setting)

    def parse_json(self, input):
        if len(input) == 0:
            return

        text = None

        try:
            obj = json.loads(input)

            text = json.dumps(
                obj,
                indent=self.settings.get('indent_width'),
                sort_keys=self.settings.get('sort_keys'),
                separators=(self.settings.get('item_seperator'),
                            self.settings.get('dictionary_seperator')))

        except ValueError:
            sublime.error_message('Malformed JSON.')

        return text

    def compact(text):
        pattern = re.compile(r'\s+')
        return re.sub(pattern, '', text)

    def filter(self, edit, region):
        text = self.parse_json(self.view.substr(region).encode('utf-8'))

        if text is not None:

            if self.settings.get('compact'):
                text = self.compact(text)

            self.view.replace(edit, region, text.decode('utf-8'))

    def run(self, edit):
        self.load_settings()

        regions = self.view.sel()

        if len(regions) == 1 and regions[0].empty():
            regions = [sublime.Region(0, self.view.size())]

        for region in regions:
            self.filter(edit, region)
