# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import a1_pb2 as a1__pb2


class RegistryServerStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Register = channel.unary_unary(
                '/rpc.RegistryServer/Register',
                request_serializer=a1__pb2.Server.SerializeToString,
                response_deserializer=a1__pb2.Response.FromString,
                )
        self.GetServerList = channel.unary_stream(
                '/rpc.RegistryServer/GetServerList',
                request_serializer=a1__pb2.Request.SerializeToString,
                response_deserializer=a1__pb2.Server.FromString,
                )


class RegistryServerServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Register(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetServerList(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_RegistryServerServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Register': grpc.unary_unary_rpc_method_handler(
                    servicer.Register,
                    request_deserializer=a1__pb2.Server.FromString,
                    response_serializer=a1__pb2.Response.SerializeToString,
            ),
            'GetServerList': grpc.unary_stream_rpc_method_handler(
                    servicer.GetServerList,
                    request_deserializer=a1__pb2.Request.FromString,
                    response_serializer=a1__pb2.Server.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'rpc.RegistryServer', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class RegistryServer(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Register(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/rpc.RegistryServer/Register',
            a1__pb2.Server.SerializeToString,
            a1__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetServerList(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/rpc.RegistryServer/GetServerList',
            a1__pb2.Request.SerializeToString,
            a1__pb2.Server.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class ArticleServerStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.JoinServer = channel.unary_unary(
                '/rpc.ArticleServer/JoinServer',
                request_serializer=a1__pb2.Client.SerializeToString,
                response_deserializer=a1__pb2.Response.FromString,
                )
        self.LeaveServer = channel.unary_unary(
                '/rpc.ArticleServer/LeaveServer',
                request_serializer=a1__pb2.Client.SerializeToString,
                response_deserializer=a1__pb2.Response.FromString,
                )
        self.GetArticles = channel.unary_stream(
                '/rpc.ArticleServer/GetArticles',
                request_serializer=a1__pb2.ArticleRequest.SerializeToString,
                response_deserializer=a1__pb2.Article.FromString,
                )
        self.PublishArticle = channel.unary_unary(
                '/rpc.ArticleServer/PublishArticle',
                request_serializer=a1__pb2.ArticleRequest.SerializeToString,
                response_deserializer=a1__pb2.Response.FromString,
                )


class ArticleServerServicer(object):
    """Missing associated documentation comment in .proto file."""

    def JoinServer(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def LeaveServer(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetArticles(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def PublishArticle(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ArticleServerServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'JoinServer': grpc.unary_unary_rpc_method_handler(
                    servicer.JoinServer,
                    request_deserializer=a1__pb2.Client.FromString,
                    response_serializer=a1__pb2.Response.SerializeToString,
            ),
            'LeaveServer': grpc.unary_unary_rpc_method_handler(
                    servicer.LeaveServer,
                    request_deserializer=a1__pb2.Client.FromString,
                    response_serializer=a1__pb2.Response.SerializeToString,
            ),
            'GetArticles': grpc.unary_stream_rpc_method_handler(
                    servicer.GetArticles,
                    request_deserializer=a1__pb2.ArticleRequest.FromString,
                    response_serializer=a1__pb2.Article.SerializeToString,
            ),
            'PublishArticle': grpc.unary_unary_rpc_method_handler(
                    servicer.PublishArticle,
                    request_deserializer=a1__pb2.ArticleRequest.FromString,
                    response_serializer=a1__pb2.Response.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'rpc.ArticleServer', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ArticleServer(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def JoinServer(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/rpc.ArticleServer/JoinServer',
            a1__pb2.Client.SerializeToString,
            a1__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def LeaveServer(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/rpc.ArticleServer/LeaveServer',
            a1__pb2.Client.SerializeToString,
            a1__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetArticles(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/rpc.ArticleServer/GetArticles',
            a1__pb2.ArticleRequest.SerializeToString,
            a1__pb2.Article.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def PublishArticle(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/rpc.ArticleServer/PublishArticle',
            a1__pb2.ArticleRequest.SerializeToString,
            a1__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
