from __future__ import unicode_literals, division, absolute_import
import os
import logging
from flexget.plugin import register_plugin, register_parser_option, priority
from flexget.utils.tools import console
from flexget.utils.template import render_from_entry, get_template

log = logging.getLogger('dump')
PLUGIN_NAME = 'make_nfo'

class OutputNfo:
    """
    Write nfo for accepetd entries.

    Example::

        presets:
          global:
            make_nfo: "{{movedone}}/{{content_filename}}.nfo"
    
    You can also specify a template::

        presets:
          global:
            make_nfo: 
              file: "{{movedone}}/{{content_filename}}.nfo"
              template: default

    File and template can also be entry specific
    """
    schema = {
        'oneOf': [
            {'type': 'string'},  # TODO: path / file
            {
                'type': 'object',
                'properties': {
                'template': {'type': 'string'},
                'file': {'type': 'string'}
            },
            'required': ['file'],
            'additionalProperties': False
            }
        ]
    }
    def __init__(self):
        pass

    def on_task_output(self, task, config):
        # Use the default template if none is specified
        if not isinstance(config, dict):
            config = {'file': config}
        if not config.get('template'):
            config['template'] = 'default.template'

        for entry in task.entries:
            outfile = entry.render(entry.get('nfo_file', config['file']))
            template = entry.get('nfo_template', config['template'])

            nfo = render_from_entry(get_template(template, PLUGIN_NAME), entry)
            
            out_dir = os.path.dirname(outfile)
            if not os.path.exists(out_dir):
                os.makedirs(out_dir)
            with open(outfile, "w") as nfo_file:
                nfo_file.write(nfo.encode('utf8'))
            entry['nfo_outfile'] = outfile
        # Output to config directory if absolute path has not been specified
        #if not os.path.isabs(output):
        #    output = os.path.join(task.manager.config_base, output)
        #if not opts.get('content_filename'):
        #    raise Exception()
        # create the template
        #template = render_from_task(get_template(filename, PLUGIN_NAME), task)

        #log.verbose('Writing output html to %s' % output)
        #with open(output, 'w') as f:
        #    f.write(template.encode('utf-8'))

register_plugin(OutputNfo, PLUGIN_NAME, api_ver=2)
