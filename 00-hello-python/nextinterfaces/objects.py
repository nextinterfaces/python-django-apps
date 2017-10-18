class molecule:

  def __init__(self,name='Generic'):
    self.name = name
    self.atomlist = []

  def addatom(self,atom):
    self.atomlist.append(atom)

  def __repr__(self):
    str = 'This is a molecule named %s\n' % self.name
    str = str+'It has %d atoms\n' % len(self.atomlist)
    for atom in self.atomlist:
      str = str + `atom` + '\n'
    return str