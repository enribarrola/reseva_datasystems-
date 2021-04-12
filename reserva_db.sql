-- phpMyAdmin SQL Dump
-- version 4.9.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 12-04-2021 a las 22:39:16
-- Versión del servidor: 10.4.8-MariaDB
-- Versión de PHP: 7.3.11

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `reserva_db`
--

DELIMITER $$
--
-- Procedimientos
--
CREATE DEFINER=`root`@`localhost` PROCEDURE `mostrarReservaID` (IN `id_res` INT)  BEGIN
select reservas.id_reserva, salas.id_sala, salas.descripcion,
DATE_FORMAT(reservas.fecha,'%Y-%m-%d') AS DATE,
DATE_FORMAT(reservas.hora_inicio,'%H:%i')TIMEONLY, 
DATE_FORMAT(reservas.hora_final,'%H:%i')Ytime from reservas 
INNER JOIN salas
ON reservas.id_sala = salas.id_sala WHERE id_reserva = id_res;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `mostrarReservas` (IN `fecha2` DATE, IN `sala_id` INT)  BEGIN

SELECT id_reserva,TIME_FORMAT(hora_inicio, "%H:%i" ),TIME_FORMAT(hora_final, "%H:%i" )FROM reservas WHERE fecha=fecha2 AND id_sala = sala_id;

END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `mostrarReservasUpdate` (IN `fecha2` DATE, IN `sala_id` INT, IN `reserva_id` INT)  BEGIN

SELECT id_reserva,TIME_FORMAT(hora_inicio, "%H:%i" ),TIME_FORMAT(hora_final, "%H:%i" )FROM reservas WHERE fecha=fecha2 AND id_sala = sala_id and id_reserva != reserva_id;

END$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `reservas`
--

CREATE TABLE `reservas` (
  `id_reserva` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `id_sala` int(11) NOT NULL,
  `fecha` date NOT NULL,
  `hora_inicio` time NOT NULL,
  `hora_final` time NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `reservas`
--

INSERT INTO `reservas` (`id_reserva`, `id_usuario`, `id_sala`, `fecha`, `hora_inicio`, `hora_final`) VALUES
(8, 12, 2, '2021-04-10', '08:00:00', '12:00:00'),
(11, 12, 1, '2021-04-11', '08:00:00', '09:30:00'),
(12, 13, 2, '2021-04-20', '08:00:00', '12:00:00'),
(13, 14, 2, '2021-04-15', '08:00:00', '15:00:00'),
(14, 19, 1, '2021-04-16', '08:06:00', '12:00:00'),
(15, 14, 2, '2021-04-16', '09:00:00', '13:00:00'),
(16, 17, 1, '2021-04-24', '08:00:00', '13:00:00'),
(17, 12, 2, '2021-04-19', '09:00:00', '16:00:00'),
(18, 16, 1, '2021-04-20', '08:00:00', '10:00:00'),
(19, 13, 1, '2021-04-23', '08:00:00', '16:00:00'),
(20, 19, 1, '2021-04-26', '06:00:00', '12:00:00'),
(21, 17, 2, '2021-04-29', '09:00:00', '16:00:00'),
(22, 15, 2, '2021-04-30', '09:00:00', '16:00:00');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `salas`
--

CREATE TABLE `salas` (
  `id_sala` int(11) NOT NULL,
  `descripcion` varchar(30) NOT NULL,
  `capacidad` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `salas`
--

INSERT INTO `salas` (`id_sala`, `descripcion`, `capacidad`) VALUES
(1, 'Standard', 40),
(2, 'Premium', 90);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id_usuario` int(11) NOT NULL,
  `nombre` varchar(30) NOT NULL,
  `apellido` varchar(30) NOT NULL,
  `correo` varchar(50) NOT NULL,
  `contraseña` varchar(30) NOT NULL,
  `tipo_usuario` int(11) NOT NULL,
  `ci_usuario` int(11) NOT NULL,
  `cel_usuario` varchar(15) NOT NULL,
  `direccion` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id_usuario`, `nombre`, `apellido`, `correo`, `contraseña`, `tipo_usuario`, `ci_usuario`, `cel_usuario`, `direccion`) VALUES
(12, 'enrique', 'fleitas', 'enri@gmail.com', '99.yoloco', 1, 4499190, '0983492073', 'lapachal 1'),
(13, 'sofia', 'rodriguez', 'sofi@gmail.com', '99.ekkojg', 1, 5939120, '0991897623', 'av humaita'),
(14, 'Lola', 'Fernandez', 'lolencia@gmai.com', 'perro', 1, 123456, '0981123123', 'mi casa'),
(15, 'Eusebio', 'Gonzales', 'eusebio123@gmail.com', '12584', 1, 1236598, '0993584621', 'yvagami 123 asuncion'),
(16, 'Gustavo', 'Otazu', 'gusta@gmail.com', '123456', 1, 8456321, '0996321548', 'agustin pio barrios calle 123'),
(17, 'Lucas ', 'Artruz', 'lucasa@gmail.com', '1236854ga', 1, 3258965, '0993846321', 'capiata km 236'),
(18, 'Edgar', 'Acosta', 'edgarcito@gmail.com', 'megustael12', 1, 9842365, '0996854652', 'brasilia casi manduvira 125'),
(19, 'Fernando ', 'Gonzales', 'fer@gmail.com', '3658', 1, 8451632, '0993874326', 'Luque calle katupiri 265');

-- --------------------------------------------------------

--
-- Estructura Stand-in para la vista `vista_reservas`
-- (Véase abajo para la vista actual)
--
CREATE TABLE `vista_reservas` (
`id_reserva` int(11)
,`descripcion` varchar(30)
,`nombre` varchar(30)
,`apellido` varchar(30)
,`DATE` varchar(10)
,`TIMEONLY` varchar(10)
,`time` varchar(10)
);

-- --------------------------------------------------------

--
-- Estructura para la vista `vista_reservas`
--
DROP TABLE IF EXISTS `vista_reservas`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `vista_reservas`  AS  select `reservas`.`id_reserva` AS `id_reserva`,`salas`.`descripcion` AS `descripcion`,`usuarios`.`nombre` AS `nombre`,`usuarios`.`apellido` AS `apellido`,date_format(`reservas`.`fecha`,'%d-%m-%Y') AS `DATE`,date_format(`reservas`.`hora_inicio`,'%H:%i') AS `TIMEONLY`,date_format(`reservas`.`hora_final`,'%H:%i') AS `time` from ((`reservas` join `usuarios` on(`reservas`.`id_usuario` = `usuarios`.`id_usuario`)) join `salas` on(`reservas`.`id_sala` = `salas`.`id_sala`)) where `reservas`.`fecha` >= (select curdate()) ;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `reservas`
--
ALTER TABLE `reservas`
  ADD PRIMARY KEY (`id_reserva`),
  ADD KEY `id_usuario` (`id_usuario`),
  ADD KEY `id_sala` (`id_sala`);

--
-- Indices de la tabla `salas`
--
ALTER TABLE `salas`
  ADD PRIMARY KEY (`id_sala`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id_usuario`),
  ADD UNIQUE KEY `ci_usuario` (`ci_usuario`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `reservas`
--
ALTER TABLE `reservas`
  MODIFY `id_reserva` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT de la tabla `salas`
--
ALTER TABLE `salas`
  MODIFY `id_sala` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id_usuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `reservas`
--
ALTER TABLE `reservas`
  ADD CONSTRAINT `reservas_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`),
  ADD CONSTRAINT `reservas_ibfk_2` FOREIGN KEY (`id_sala`) REFERENCES `salas` (`id_sala`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
