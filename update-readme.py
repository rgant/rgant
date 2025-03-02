#!/usr/bin/env python
"""
Download the SVG files from [skill-icons](LelouchFR/skill-icons), update README with skill icons and
links.

> [!IMPORTANT]
> I've decided to handle updating local cache by deleting the files. But then I won't know if any of
> the local icons need updates... so maybe reconsider?
"""
import glob
import http.client
import logging
import os
import pathlib
import re
import typing
import urllib.request
import xml.dom.minidom


Skill = typing.TypedDict(
    'Skill',
    {
        'img_key': str,
        'link': str,
        'name': str,
    },
)


SKILLS: list[Skill] = [
    # Basic web techs
    {
        'img_key': 'html',
        'link': 'https://developer.mozilla.org/en-US/docs/Web/HTML',
        'name': 'HTML',
    },
    {
        'img_key': 'css',
        'link': 'https://developer.mozilla.org/en-US/docs/Web/CSS',
        'name': 'CSS',
    },
    {
        'img_key': 'sass',
        'link': 'https://sass-lang.com/',
        'name': 'Sass / SCSS',
    },
    {
        'img_key': 'bootstrap',
        'link': 'https://getbootstrap.com/',
        'name': 'Bootstrap',
    },
    {
        'img_key': 'typescript',
        'link': 'https://www.typescriptlang.org/',
        'name': 'TypeScript',
    },
    {
        'img_key': 'javascript',
        'link': 'https://developer.mozilla.org/en-US/docs/Web/JavaScript',
        'name': 'JavaScript',
    },
    # Web frameworks and tools
    {
        'img_key': 'angular',
        'link': 'https://angular.dev/',
        'name': 'Angular',
    },
    {
        'img_key': 'cypress',
        'link': 'https://www.cypress.io/',
        'name': 'Cypress',
    },
    {
        'img_key': 'karma',
        'link': 'https://karma-runner.github.io/latest/index.html',
        'name': 'Karma',
    },
    {
        'img_key': 'jasmine',
        'link': 'https://jasmine.github.io/',
        'name': 'Jasmine',
    },
    {
        'img_key': 'jest',
        'link': 'https://jestjs.io/',
        'name': 'Jest',
    },
    {
        'img_key': 'react',
        'link': 'https://react.dev/',
        'name': 'React',
    },
    {
        'img_key': 'vuejs',
        'link': 'https://vuejs.org/',
        'name': 'Vue.js',
    },
    {
        'img_key': 'jquery',
        'link': 'https://jquery.com/',
        'name': 'jQuery',
    },
    # Python tools
    {
        'img_key': 'python',
        'link': 'https://www.python.org/',
        'name': 'Python',
    },
    {
        'img_key': 'pytest',
        'link': 'https://docs.pytest.org/en/stable/',
        'name': 'pytest',
    },
    {
        'img_key': 'fastapi',
        'link': 'https://fastapi.tiangolo.com/',
        'name': 'FastAPI',
    },
    {
        'img_key': 'flask',
        'link': 'https://flask.palletsprojects.com/en/stable/',
        'name': 'Flask',
    },
    {
        'img_key': 'sqlalchemy',
        'link': 'https://www.sqlalchemy.org/',
        'name': 'SQLAlchemy',
    },
    {
        'img_key': 'django',
        'link': 'https://www.djangoproject.com/',
        'name': 'Django',
    },
    {
        'img_key': 'numpy',
        'link': 'https://numpy.org/',
        'name': 'NumPy',
    },
    {
        'img_key': 'pytorch',
        'link': 'https://pytorch.org/',
        'name': 'PyTorch',
    },
    {
        'img_key': 'tensorflow',
        'link': 'https://www.tensorflow.org/',
        'name': 'TensorFlow',
    },
    # Server stuff
    {
        'img_key': 'nodejs',
        'link': 'https://nodejs.org/',
        'name': 'Node.js',
    },
    {
        'img_key': 'expressjs',
        'link': 'https://expressjs.com/',
        'name': 'Express',
    },
    {
        'img_key': 'nestjs',
        'link': 'https://nestjs.com/',
        'name': 'NestJS',
    },
    {
        'img_key': 'nextjs',
        'link': 'https://nextjs.org/',
        'name': 'Next.js',
    },
    {
        'img_key': 'api',
        'link': 'https://jsonapi.org/format/',
        'name': 'JSON:API',
    },
    {
        'img_key': 'graphql',
        'link': 'https://graphql.org/',
        'name': 'GraphQL',
    },
    {
        'img_key': 'nginx',
        'link': 'https://nginx.org/',
        'name': 'nginx',
    },
    # Databases
    {
        'img_key': 'postgresql',
        'link': 'https://www.postgresql.org/',
        'name': 'PostgreSQL',
    },
    {
        'img_key': 'mongodb',
        'link': 'https://www.mongodb.com/',
        'name': 'MongoDB',
    },
    {
        'img_key': 'mysql',
        'link': 'https://www.mysql.com/',
        'name': 'MySQL',
    },
    {
        'img_key': 'mariadb',
        'link': 'https://mariadb.org/',
        'name': 'MariaDB',
    },
    {
        'img_key': 'redis',
        'link': 'https://redis.io/',
        'name': 'Redis',
    },
    {
        'img_key': 'sqlite',
        'link': 'https://www.sqlite.org/',
        'name': 'SQLite',
    },
    # DevOps and clouds
    {
        'img_key': 'docker',
        'link': 'https://www.docker.com/',
        'name': 'Docker',
    },
    {
        'img_key': 'terraform',
        'link': 'https://www.terraform.io/',
        'name': 'Terraform',
    },
    {
        'img_key': 'aws',
        'link': 'https://aws.amazon.com/',
        'name': 'Amazon Web Services (AWS)',
    },
    {
        'img_key': 'gcp',
        'link': 'https://cloud.google.com/',
        'name': 'Google Cloud Platform (GCP)',
    },
    {
        'img_key': 'firebase',
        'link': 'https://firebase.google.com/',
        'name': 'Firebase',
    },
    {
        'img_key': 'azure',
        'link': 'https://azure.microsoft.com/en-us/',
        'name': 'Microsoft Azure',
    },
    {
        'img_key': 'heroku',
        'link': 'https://www.heroku.com/',
        'name': 'Heroku',
    },
    # CLI tools
    {
        'img_key': 'bash',
        'link': 'https://www.gnu.org/software/bash/',
        'name': 'Bash',
    },
    {
        'img_key': 'bsd',
        'link': 'https://www.freebsd.org/',
        'name': 'FreeBSD',
    },
    {
        'img_key': 'linux',
        'link': 'https://www.linux.org/',
        'name': 'Linux',
    },
    {
        'img_key': 'npm',
        'link': 'https://www.npmjs.com/',
        'name': 'npm',
    },
    {
        'img_key': 'yarn',
        'link': 'https://yarnpkg.com/',
        'name': 'Yarn',
    },
    {
        'img_key': 'pnpm',
        'link': 'https://pnpm.io/',
        'name': 'pnPm',
    },
    {
        'img_key': 'regex',
        'link': 'https://www.regular-expressions.info/',
        'name': 'Regular Expressions',
    },
    # Version control and editors
    {
        'img_key': 'git',
        'link': 'https://git-scm.com/',
        'name': 'Git',
    },
    {
        'img_key': 'github',
        'link': 'https://github.com/',
        'name': 'GitHub',
    },
    {
        'img_key': 'bitbucket',
        'link': 'https://bitbucket.org/product/',
        'name': 'Bitbucket',
    },
    {
        'img_key': 'gitlab',
        'link': 'https://about.gitlab.com/',
        'name': 'GitLab',
    },
    {
        'img_key': 'sublime',
        'link': 'https://www.sublimetext.com/',
        'name': 'Sublime Text',
    },
    {
        'img_key': 'firefox',
        'link': 'https://www.mozilla.org/en-US/firefox/',
        'name': 'Firefox',
    },
]


def build_readme() -> None:
    """Combine components to create README.md"""
    files = sorted(os.listdir('./components'))

    readme_content = ''
    for filename in files:
        with open(f'./components/{filename}', 'r') as source_file:
            readme_content += source_file.read()
            # Don't want two newlines at the end of the file
            if filename != files[-1]:
                readme_content += '\n'

    with open('./README.md', 'w') as readme_file:
        _ = readme_file.write(readme_content)


def build_skills(skills: list[list[Skill]]) -> None:
    """Add skills to the skills component."""
    skills_filename = glob.glob('./components/*.skills.md')[0]
    with open(skills_filename, 'w') as skills_file:
        _ = skills_file.write('## Languages and Tools\n\n')

        for chunk in skills:
            for skill in chunk:
                content = get_skill_markdown(skill)
                # Markdown line break is `\` at the end of the line. Otherwise one newline will wrap
                lineending = '\\\n' if skill == chunk[-1] and chunk != skills[-1] else '\n'
                _ = skills_file.write(f'{content}{lineending}')


def cache_icons(skills: list[Skill]) -> None:
    """"""
    logger = logging.getLogger(__name__)
    local_assets_map = get_local_asset_map()

    # Only update if there are skills with missing icons.
    needs_update = icons_need_update(skills, local_assets_map)
    if needs_update:
        skill_asset_map = get_skill_asset_map()

        for skill in skills:
            if skill['img_key'] not in local_assets_map:
                try:
                    url = skill_asset_map[skill['img_key']]
                except KeyError:
                    logger.warning('No Asset for %r', skill["img_key"])
                else:
                    fetch_icon(url, skill['img_key'])


def chunk_skills(skills: list[Skill]) -> list[list[Skill]]:
    """Find the best split for the current number of skills."""

    class PossibleSplits(typing.NamedTuple):
        remainder: int
        cnt: int

    num_skills = len(skills)
    # range counts from 8 to 14 (the stop parameter is exclusive)
    possible_splits = [PossibleSplits(num_skills % cnt, cnt) for cnt in range(8, 15)]

    # Order the splits first by smallest remaining, then by largest count.
    best_split = sorted(possible_splits, key=lambda x: (x.remainder, -x.cnt))[0].cnt

    # Chunks skills list into best_split sizes
    return [skills[i : i + best_split] for i in range(0, len(skills), best_split)]


def fetch_icon(url: str, img_key: str) -> None:
    """
    1. Retrieve the icon from LelouchFR/skill-icons
    2. Apply our customizations (size to 48px square)
    3. ~Apply optimization~ I looked into using [scour](https://github.com/scour-project/scour), but
       found that it didn't really optimize as well as svgo. So I'll just run that manually.
    """
    local_filename, _ = urllib.request.urlretrieve(url)

    with open(local_filename, 'r') as tmp_svg_file:
        svg_dom = xml.dom.minidom.parse(tmp_svg_file)

    os.remove(local_filename)

    svg_node = svg_dom.getElementsByTagName('svg')[0]
    svg_node.setAttribute('width', '48')
    svg_node.setAttribute('height', '48')

    with open(f'./assets/{img_key}.svg', 'w') as svg_file:
        svg_dom.writexml(svg_file)


def get_local_asset_map() -> dict[str, str]:
    """Lookup local asset files and identify the img_key for them."""

    def key_from_file(filename: str) -> str:
        """basename without extension of the filename is the img_key"""
        return pathlib.Path(filename).stem

    return {key_from_file(filename): filename for filename in glob.glob('./assets/*.svg')}


def get_raw_url(path: str) -> str:
    """
    Convert the relative URL from the LelouchFR README.md file into a raw.githubusercontent url.
    """
    prefix = 'https://raw.githubusercontent.com/LelouchFR/skill-icons/refs/heads/main'

    # Get the dark version of the icons
    if path.endswith('-auto.svg'):
        return f'{prefix}{path.replace("-auto.", "-dark.")}'

    return f'{prefix}{path}'


def get_skill_asset_map() -> dict[str, str]:
    """
    Download the LelouchFR README.md file and construct a map of skill key to remote image URL.
    """
    readme_url = 'https://raw.githubusercontent.com/LelouchFR/skill-icons/refs/heads/main/README.md'
    response: http.client.HTTPResponse
    with urllib.request.urlopen(readme_url) as response:
        readme = response.read().decode()

    asset_pttrn = re.compile(r'\|\s*`(\w+)`\s*\|\s*<img src="\.(/assets/.*?)"')
    ret = {match[1]: get_raw_url(match[2]) for match in asset_pttrn.finditer(readme)}
    return ret


def get_skill_markdown(skill: Skill) -> str:
    """Create the markdown for the skill"""
    return (
        f'['  # Start of link around image
        f'![{skill["name"]}](./assets/{skill["img_key"]}.svg)'  # Embed image
        f']({skill["link"]})'  # Link to skill homepage
    )


def icons_need_update(skills: list[Skill], assets: dict[str, str]) -> bool:
    """Check the skills list with the local assets to see if there is any need to update."""
    for skill in skills:
        if skill['img_key'] not in assets:
            return True

    return False


def main() -> None:
    """
    1. Cache local copies of the skill icons from LelouchFR/skill-icons
    2. Update the skills.md component with the skills markdown.
    3. Construct the README.md from the component files.
    """
    cache_icons(SKILLS)
    chunks = chunk_skills(SKILLS)
    build_skills(chunks)
    build_readme()
    print('''Use `svgo` to optimize the icons. Dependencies is located in rob.gant.ninja project''')


if __name__ == '__main__':
    logging.basicConfig()#level=logging.INFO)
    main()
