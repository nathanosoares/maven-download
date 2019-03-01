import os
from xml.etree import ElementTree as et


def parseid(group, artifact):
    return '%s@%s' % (group, artifact)


def createtree(pom_filename):
    tree = et.ElementTree()
    tree.parse(pom_filename)
    return tree


def findid(pom_filename):
    if os.path.exists(pom_filename) == False:
        return None

    tree = createtree(pom_filename)

    parent = tree.getroot().find("{%s}parent" % ns)

    if parent is not None:
        if parent.find('{%s}groupId' % ns) is not None:
            group = parent.find('{%s}groupId' % ns).text

    if tree.getroot().find('{%s}groupId' % ns) is not None:
        group = tree.getroot().find('{%s}groupId' % ns).text

    if tree.getroot().find('{%s}artifactId' % ns) is not None:
        artifact = tree.getroot().find('{%s}artifactId' % ns).text

    return parseid(group, artifact)


def finddependencies(pom_filename):
    out = []

    tree = createtree(pom_filename)

    dependencies = tree.getroot().find('{%s}dependencies' % ns)

    if dependencies is not None:
        for dependency in list(dependencies):
            group = dependency.find('{%s}groupId' % ns).text
            artifact = dependency.find('{%s}artifactId' % ns).text
            out.append(parseid(group, artifact))

    return out


def findmodules(pom_filename):
    out = []

    tree = createtree(pom_filename)
    modules = tree.getroot().find('{%s}modules' % ns)

    if modules is not None:
        for module in list(modules):
            out.append(module.text)

    return out


current_dirname = os.path.dirname(os.path.abspath(__file__))
projects_dirname = '{0}/tests'.format(current_dirname)

ns = "http://maven.apache.org/POM/4.0.0"

mapped = {}

for project_name in os.listdir(projects_dirname):

    project_dir = '{0}/{1}'.format(projects_dirname, project_name)
    pom_filename = '{0}/pom.xml'.format(project_dir)

    if os.path.exists(pom_filename) == False:
        continue

    modules = findmodules(pom_filename)

    for module_name in modules:
        module_pom_filename = '%s/%s/pom.xml' % (project_dir, module_name)
        
        if os.path.exists(module_pom_filename) == False:
            continue

        dependencies = finddependencies(module_pom_filename)
        mapped[findid(module_pom_filename)] = dependencies

    dependencies = finddependencies(pom_filename)

    if dependencies:
        mapped[findid(pom_filename)] = dependencies


print(mapped)
compiled = []

while len(compiled) < len(mapped):
    for project, dependencies in mapped:
        if project in compiled:
            continue
        
        depends = False

        for project2 in mapped:
            if (project2 not in compiled) and (project2 in dependencies):
                depends = True
                break

        if not depends:
            compiled.insert(project)
            #compilar o projeto


print(mapped)
