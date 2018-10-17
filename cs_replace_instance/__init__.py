# python
import modo
import lx

from commander import *


def get_meshes(scene):
    """
    Gets the meshes we need to start the script running
    :param scene: The modo.Scene module for the scene
    :return: list [ instances, replacement_mesh, original_mesh ]
    """
    # all the instances we want to duplicate and change the source
    instances = []
    # the mesh we want to use as the new source
    replacement_mesh = None
    # the original mesh
    original_mesh = None

    for item in scene.selected:
        if item.isAnInstance:
            instances.append(item)
            original_mesh = item.itemGraph("meshInst").connectedItems["Reverse"][0]
        else:
            replacement_mesh = item
    return [instances, replacement_mesh, original_mesh]


def update_xforms(instances, duplicate_instances):
    for original, duplicate in zip(instances, duplicate_instances):
        # set the duplicates xforms to the be the same as the original xforms
        # pos
        pos = modo.LocatorSuperType(original).position
        modo.LocatorSuperType(duplicate).position.x.set(pos.x.get())
        modo.LocatorSuperType(duplicate).position.y.set(pos.y.get())
        modo.LocatorSuperType(duplicate).position.z.set(pos.z.get())
        # rot
        rot = modo.LocatorSuperType(original).rotation
        modo.LocatorSuperType(duplicate).rotation.x.set(rot.x.get())
        modo.LocatorSuperType(duplicate).rotation.y.set(rot.y.get())
        modo.LocatorSuperType(duplicate).rotation.z.set(rot.z.get())
        # scale
        scale = modo.LocatorSuperType(original).scale
        modo.LocatorSuperType(duplicate).scale.x.set(scale.x.get())
        modo.LocatorSuperType(duplicate).scale.y.set(scale.y.get())
        modo.LocatorSuperType(duplicate).scale.z.set(scale.z.get())


def main():
    scene = modo.Scene()
    instances, replacement_mesh, original_mesh = get_meshes(scene)
    duplicate_original = scene.duplicateItem(original_mesh)
    duplicate_original.name = replacement_mesh.name + "_RI"
    duplicate_instances = []
    for i in instances:
        item = scene.duplicateItem(duplicate_original, True)
        item.name = i.name + "_RI"
        duplicate_instances.append(item)
        # update the xforms to match those of the original instance
    update_xforms(instances, duplicate_instances)
    # replace the duplicate original with the replacement mesh
    scene.select(replacement_mesh)
    lx.eval("select.typeFrom polygon")
    lx.eval("select.all")
    lx.eval("copy")
    scene.select(duplicate_original)
    lx.eval("select.all")
    lx.eval("delete")
    lx.eval("paste")
    # put them into a group
    grp = scene.addItem(
        modo.constants.GROUPLOCATOR_TYPE, name=replacement_mesh.name + "_RI_GROUP"
    )
    duplicate_original.setParent(grp)
    for i in duplicate_instances:
        i.setParent(grp)
    # select the new group we just added so they know what happened
    scene.select(grp)


if __name__ == "__main__":
    main()
