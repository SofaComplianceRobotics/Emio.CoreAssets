def createScene(rootnode):
    from utils.header import addHeader, addSolvers
    from parts.leg import Leg

    # Header of the simulation
    settings, modelling, simulation = addHeader(rootnode, withCollision=False)
    rootnode.dt = 0.01
    rootnode.gravity = [0., -98100., 0.]
    addSolvers(simulation)

    settings.addObject('RequiredPlugin', pluginName='Sofa.Component.Constraint.Projective')
    rootnode.VisualStyle.displayFlags = ["showWireframe", "showBehavior"]
    # Needed to use components [FixedProjectiveConstraint]

    # Leg
    for model in ['beam', 'tetra']:
        leg = Leg(name=model+"Leg",
                  legName="blueleg",
                  positionOnMotor="clockwisedown",
                  model=model,
                  youngModulus=3e5,
                  poissonRatio=0.3,
                  massdensity=1.22e-6,
                  rotation=[90, 0, 0]
                  )
        simulation.addChild(leg)
        leg.base.addObject("FixedProjectiveConstraint", indices=[0])

    return
