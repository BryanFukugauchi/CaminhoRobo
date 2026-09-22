'''
Aluno: Bryan Massahiro Duran Fukugauchi - RA: 24120
'''
from controller import Robot


robot = Robot()
timestep = int(robot.getBasicTimeStep())

print("Iniciando motores, sensores e câmera...")

motorE = robot.getDevice('motorE')
motorD = robot.getDevice('motorD')

if motorE is None or motorD is None:
    print("ERRO: Verifique os nomes 'motorE' e 'motorD' no Webots.")

motorE.setPosition(float('inf'))
motorD.setPosition(float('inf'))
motorE.setVelocity(0.0)
motorD.setVelocity(0.0)

dsd = robot.getDevice('DSD')
dse = robot.getDevice('DSE')

if dsd is None or dse is None:
    print("ERRO: Verifique os nomes 'DSD' e 'DSE' no Webots.")
else:
    dsd.enable(timestep)
    dse.enable(timestep)

camera = robot.getDevice('camera')

if camera is None:
    print("ERRO: Câmera não encontrada! Verifique o nome no Scene Tree.")
else:
    camera.enable(timestep)
    print(f"Câmera ativada com resolução {camera.getWidth()}x{camera.getHeight()}")

VELOCIDADE = 2.5
VELOCIDADE_CURVA = 1.8
LIMIAR = 500

ultima_direcao = 0

while robot.step(timestep) != -1:

    if camera is not None:
        imagem = camera.getImage()

    ve = dse.getValue()
    vd = dsd.getValue()
    print(f"Esquerdo: {ve:.1f} | Direito: {vd:.1f}")

    esquerdo_preto = ve > LIMIAR
    direito_preto = vd > LIMIAR

    if esquerdo_preto and direito_preto:
        motorE.setVelocity(VELOCIDADE)
        motorD.setVelocity(VELOCIDADE)

    elif esquerdo_preto and not direito_preto:
        motorE.setVelocity(VELOCIDADE_CURVA)
        motorD.setVelocity(VELOCIDADE)
        ultima_direcao = -1

    elif direito_preto and not esquerdo_preto:
        motorE.setVelocity(VELOCIDADE)
        motorD.setVelocity(VELOCIDADE_CURVA)
        ultima_direcao = 1

    else:
        if ultima_direcao == -1:
            motorE.setVelocity(0)
            motorD.setVelocity(1.5)
        elif ultima_direcao == 1:
            motorE.setVelocity(1.5)
            motorD.setVelocity(0)
        else:
            motorE.setVelocity(1.0)
            motorD.setVelocity(1.0)