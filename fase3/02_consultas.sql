-- FarmTech Solutions - Fase 3 - Cap 1
-- Consultas para evidenciar a carga da base de sensores no Oracle.

-- 1) Consulta geral solicitada no enunciado.
SELECT *
FROM leituras_alface;

-- 2) Conferencia do total de registros importados.
SELECT COUNT(*) AS total_leituras
FROM leituras_alface;

-- 3) Quantidade de leituras por status da bomba.
SELECT bomba_status, COUNT(*) AS total
FROM leituras_alface
GROUP BY bomba_status
ORDER BY total DESC;

-- 4) Medias dos principais sensores monitorados.
SELECT
    ROUND(AVG(ph_estimado), 2) AS ph_medio,
    ROUND(AVG(umidade_pct), 2) AS umidade_media,
    ROUND(AVG(temperatura_c), 2) AS temperatura_media
FROM leituras_alface;

-- 5) Leituras em que a bomba ligou porque todos os criterios estavam adequados.
SELECT
    id_leitura,
    data_hora,
    ph_estimado,
    umidade_pct,
    temperatura_c,
    bomba_status,
    recomendacao
FROM leituras_alface
WHERE bomba_status = 'LIGADA'
ORDER BY id_leitura;

-- 6) Casos em que o NPK impediu a irrigacao.
SELECT
    id_leitura,
    data_hora,
    n_presente,
    p_presente,
    k_presente,
    recomendacao
FROM leituras_alface
WHERE nutrientes_ok = 0
ORDER BY id_leitura;

-- 7) Casos em que o pH estimado pelo LDR ficou fora da faixa ideal da alface.
SELECT
    id_leitura,
    data_hora,
    ldr_raw,
    ph_estimado,
    recomendacao
FROM leituras_alface
WHERE ph_ok = 0
ORDER BY ph_estimado;

-- 8) Resumo por recomendacao agronomica.
SELECT recomendacao, COUNT(*) AS total
FROM leituras_alface
GROUP BY recomendacao
ORDER BY total DESC;
