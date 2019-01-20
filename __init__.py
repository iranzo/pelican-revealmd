import subprocess

from pelican import signals
from pelican.readers import BaseReader, MarkdownReader


class RevealJSMarkdownReader(BaseReader):
    """Reads a markdown document and converts it to a reveal.js presentation

    http://docs.getpelican.com/en/stable/plugins.html#how-to-create-a-new-reader
    """
    enabled = True
    file_extensions = ["revealjs"]

    def read(self, filename):
        """Convert a revealjs markdown file to html and return it

        Requires pypandoc (https://github.com/bebraw/pypandoc) and pandoc
        (https://pandoc.org/) to work correctly.
        """

        # TODO: use markdown reader to parse the reveal.js markdown
        # https://github.com/danielfrg/pelican-ipynb/blob/master/markup.py#L62
        reader = MarkdownReader(self.settings)
        md_content, metadata = reader.read(filename)

        # TODO: using the markdown reader converts the file contents to HTML,
        # but we just want plain text because pandoc should be converting it
        # instead. The trouble is, we also want to get the metadata

        commandextra = ""

        if 'theme' in metadata:
            commandextra = "--variable theme=%s" % metadata['theme']

        if 'revealoptions' in metadata:
            if 'transition' in metadata['revealoptions']:
                commandextra = commandextra + " --variable transition=%s" % metadata['revealoptions']['transition']

        command  = "pandoc --to revealjs -f markdown %s %s" % (filename, commandextra)

        # Define template for Pelican
        metadata["template"] = "blank"

        p = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        try:
            stdout, stderr = p.communicate(str.encode('utf8'))
        except OSError:
            raise RuntimeError('Pandoc died with exitcode "%s" during conversion.' % p.returncode)

        revealjs_content = stdout.decode('utf8')

        # Patch revealjs_content to convert 'back' "{" and "}"
        returntext = revealjs_content.replace('%7B', '{').replace('%7D','}')

        return returntext, metadata


def add_reader(readers):
    for extension in RevealJSMarkdownReader.file_extensions:
        readers.reader_classes[extension] = RevealJSMarkdownReader


def register():
    signals.readers_init.connect(add_reader)
